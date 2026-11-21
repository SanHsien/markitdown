"""Read spreadsheet drawing images without reloading or resaving the workbook."""

import io
import mimetypes
import posixpath
import zipfile
import zlib
from typing import Any, BinaryIO, Callable, Optional
from urllib.parse import unquote

from defusedxml import ElementTree as ET

from .._stream_info import StreamInfo
from ._image import _parse_image_html

_NS = {
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
_REL_ID = "{" + _NS["r"] + "}id"
_EMBED = "{" + _NS["r"] + "}embed"


def _relationships(
    archive: zipfile.ZipFile, part: str, kind: Optional[str] = None
) -> dict[str, str]:
    directory, filename = posixpath.split(part)
    rels = posixpath.join(directory, "_rels", filename + ".rels")
    if rels not in archive.namelist():
        return {}
    root = ET.fromstring(archive.read(rels))
    return {
        rel.attrib["Id"]: posixpath.normpath(
            posixpath.join(directory, unquote(rel.attrib["Target"]))
        ).lstrip("/")
        for rel in root
        if rel.get("TargetMode") != "External"
        and (kind is None or rel.attrib["Type"].endswith("/" + kind))
    }


_READ_CHUNK = 64 * 1024


class _ImageTooLarge(ValueError):
    def __init__(self, what: str, limit: int):
        super().__init__(f"{what} exceeds the {limit}-byte limit")


def _read_limited(archive: zipfile.ZipFile, part: str, limit: int) -> bytes:
    """Read a member in bounded chunks, never holding more than ``limit + 1``.

    ``ZipFile.read`` decompresses a whole member in one call even when its
    declared size is small, so a forged size cannot be trusted for memory.
    """
    chunks = []
    total = 0
    with archive.open(part) as member:
        while True:
            chunk = member.read(min(_READ_CHUNK, limit + 1 - total))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > limit:
                raise _ImageTooLarge("decompressed data", limit)
            chunks.append(chunk)


class _XlsxImages:
    def __init__(
        self,
        file_stream: BinaryIO,
        on_unreadable: Optional[Callable[[str, Exception], None]] = None,
        max_image_bytes: Optional[int] = None,
    ):
        """Collect embedded images per sheet.

        An image whose relationship or package part is missing raises by
        default (upstream #2506). When ``on_unreadable`` is given it is called
        with the reference and the error instead; if it returns, that image
        (or, for a missing drawing part, that drawing) is skipped and
        collection continues. ``max_image_bytes`` (requires ``on_unreadable``)
        skips an image whose declared size is larger without reading it, and
        otherwise reads it in bounded chunks, abandoning it once more than
        ``max_image_bytes`` decompressed bytes appear or the member is
        corrupt (a forged smaller size ends in a CRC error).
        """
        self._sheets: dict[str, list[tuple[bytes, StreamInfo]]] = {}
        with zipfile.ZipFile(file_stream) as archive:
            workbook = _relationships(archive, "", "officeDocument")
            workbook_part = next(iter(workbook.values()))
            sheets = ET.fromstring(archive.read(workbook_part))
            sheet_parts = _relationships(archive, workbook_part)
            content_types = ET.fromstring(archive.read("[Content_Types].xml"))
            defaults = {
                item.attrib["Extension"].lower(): item.attrib["ContentType"]
                for item in content_types
                if "Extension" in item.attrib
            }
            overrides = {
                unquote(item.attrib["PartName"]).lstrip("/"): item.attrib["ContentType"]
                for item in content_types
                if "PartName" in item.attrib
            }
            for sheet in sheets.findall("s:sheets/s:sheet", _NS):
                sheet_part = sheet_parts[sheet.attrib[_REL_ID]]
                drawings = ET.fromstring(archive.read(sheet_part)).findall(
                    "s:drawing", _NS
                )
                if not drawings:
                    continue
                drawing_parts = _relationships(archive, sheet_part, "drawing")
                images = self._sheets.setdefault(sheet.attrib["name"], [])
                for drawing in drawings:
                    reference = drawing.attrib[_REL_ID]
                    try:
                        drawing_part = drawing_parts[reference]
                        drawing_xml = archive.read(drawing_part)
                    except (KeyError, zipfile.BadZipFile, zlib.error) as error:
                        if on_unreadable is None:
                            raise
                        on_unreadable(drawing_parts.get(reference, reference), error)
                        continue
                    image_parts = _relationships(archive, drawing_part, "image")
                    drawing_root = ET.fromstring(drawing_xml)
                    # Match openpyxl's image traversal, not its XML serialization order.
                    anchors = [
                        anchor
                        for kind in ("absoluteAnchor", "oneCellAnchor", "twoCellAnchor")
                        for anchor in drawing_root.findall(f"xdr:{kind}", _NS)
                    ]
                    for anchor in anchors:
                        for blip in anchor.findall(".//a:blip", _NS):
                            relationship = blip.get(_EMBED)
                            if relationship is None:
                                # Linked images are not embedded package content.
                                continue
                            try:
                                image_part = image_parts[relationship]
                                if on_unreadable is None or max_image_bytes is None:
                                    data = archive.read(image_part)
                                else:
                                    # Fast path on the declared size, then a
                                    # bounded read that does not trust it.
                                    size = archive.getinfo(image_part).file_size
                                    if size > max_image_bytes:
                                        raise _ImageTooLarge(
                                            f"declared size {size} bytes",
                                            max_image_bytes,
                                        )
                                    data = _read_limited(
                                        archive, image_part, max_image_bytes
                                    )
                            except (
                                KeyError,
                                zipfile.BadZipFile,
                                zlib.error,
                                _ImageTooLarge,
                            ) as error:
                                if on_unreadable is None:
                                    raise
                                on_unreadable(
                                    image_parts.get(relationship, relationship),
                                    error,
                                )
                                continue
                            extension = posixpath.splitext(image_part)[1].lower()
                            info = StreamInfo(
                                mimetype=overrides.get(image_part)
                                or defaults.get(extension.lstrip("."))
                                or mimetypes.guess_type(image_part)[0],
                                extension=extension,
                                filename=posixpath.basename(image_part),
                            )
                            images.append((data, info))

    def to_html(
        self,
        sheet_name: str,
        render: Callable[..., Optional[str]],
        options: dict[str, Any],
    ) -> str:
        fragments = []
        for data, info in self._sheets.get(sheet_name, []):
            with io.BytesIO(data) as image_stream:
                fragment = render(image_stream, info, **options)
            soup = _parse_image_html(fragment)
            if soup is None:
                continue
            fragments.append(f"<div>{soup}</div>")
        if not fragments:
            return ""
        return "<h3>Images in this sheet:</h3>" + "".join(fragments)
