"""XLSX image OCR using the core spreadsheet conversion pipeline."""

import hashlib
import html
from typing import Any, BinaryIO, Optional
from warnings import warn

from markitdown import DocumentConverterResult, StreamInfo
from markitdown.converters import XlsxConverter

from ._ocr_service import LLMVisionOCRService, _extract_text_with_metadata


DEFAULT_MAX_IMAGE_BYTES = 20 * 1024 * 1024


class XlsxConverterWithOCR(XlsxConverter):
    """Recognize embedded images while inheriting native XLSX conversion.

    Images larger than ``max_image_bytes`` (declared uncompressed size; None
    disables the cap) are skipped with a RuntimeWarning before being read.
    """

    def __init__(
        self,
        ocr_service: Optional[LLMVisionOCRService] = None,
        max_image_bytes: Optional[int] = DEFAULT_MAX_IMAGE_BYTES,
    ):
        super().__init__()
        if not hasattr(XlsxConverter, "_image_to_html"):
            raise RuntimeError(
                "XLSX OCR requires markitdown>=0.1.8b3 for the "
                "XlsxConverter._image_to_html hook. "
                "Upgrade with: pip install --upgrade 'markitdown>=0.1.8b3'."
            )
        self.ocr_service = ocr_service
        self.max_image_bytes = max_image_bytes

    @property
    def _max_image_bytes(self) -> Optional[int]:  # type: ignore[override]
        return self.max_image_bytes

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if not (kwargs.get("ocr_service") or self.ocr_service):
            # Without a recognizer the hook declines every image, so skip image
            # parsing: output stays exactly native, and broken or huge embedded
            # media that the native converter ignores cannot fail or bloat it.
            return XlsxConverter().convert(file_stream, stream_info, **kwargs)
        kwargs["_xlsx_ocr_cache"] = {}
        return super().convert(file_stream, stream_info, **kwargs)

    def _unreadable_image(self, reference: str, error: Exception) -> None:
        # Fork divergence: one broken or oversized image (or drawing) must not
        # discard the OCR output of every other image, or the whole workbook
        # when no builtin converter can fall back. Report it, like an OCR
        # error, and skip only it.
        warn(
            f"XLSX embedded image {reference!r} could not be read ({error}); "
            "skipping it.",
            RuntimeWarning,
            stacklevel=2,
        )

    def _image_to_html(
        self,
        image_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> Optional[str]:
        ocr_service = kwargs.get("ocr_service") or self.ocr_service
        if ocr_service is None:
            return None

        cache: dict[bytes, Optional[str]] = kwargs.get("_xlsx_ocr_cache", {})
        key = hashlib.sha256(image_stream.read()).digest()
        image_stream.seek(0)
        if key in cache:
            return cache[key]

        result = _extract_text_with_metadata(ocr_service, image_stream, stream_info)
        if result.error:
            warn(
                f"XLSX image OCR failed: {result.error}. Keeping the native image.",
                RuntimeWarning,
                stacklevel=2,
            )
            cache[key] = None
            return None
        text = result.text.strip()
        if not text:
            cache[key] = None
            return None

        text = text.replace("\r\n", "\n").replace("\r", "\n")
        content = html.escape(text).replace("\n", "<br>")
        fragment = f"<p><em>[Image OCR]<br>{content}<br>[End OCR]</em></p>"
        cache[key] = fragment
        return fragment
