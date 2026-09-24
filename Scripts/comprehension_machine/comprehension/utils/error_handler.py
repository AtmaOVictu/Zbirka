"""Three-tier error handler: Dialog + Log + Continue."""

import logging, traceback
logger = logging.getLogger(__name__)


class ErrorHandler:
    @staticmethod
    def handle(exception, context, show_dialog=True):
        error_text = str(exception)
        tb = traceback.format_exc()
        severity = context.get("severity", "error")
        if severity == "critical":
            logger.critical(f"[{context.get('module','?')}] {error_text}")
        else:
            logger.error(f"[{context.get('module','?')}] {error_text}")
        db = context.get("database")
        if db:
            try:
                db.log_error(context.get("module", "unknown"), error_text,
                             context.get("session_id", ""), context.get("phase", ""), tb, severity)
            except Exception as e:
                logger.critical(f"DB log failed: {e}")
        if show_dialog and context.get("ui_available", False):
            try:
                from PyQt6.QtWidgets import QMessageBox
                if severity == "critical":
                    QMessageBox.critical(None, "Napaka", f"{context.get('module','?')}: {error_text}")
            except ImportError:
                pass
        return {"status": "partial" if context.get("fallback") else "failed",
                "error": error_text, "fallback_data": context.get("fallback", {})}
