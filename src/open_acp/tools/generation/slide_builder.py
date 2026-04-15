"""Slide builder — generates PowerPoint slides from structured data."""
from open_acp.tools.base_tool import BaseTool, ToolResult, ToolTier, ToolStatus


class SlideBuilder(BaseTool):
    name = "slide_builder"
    capability = "generation"
    provider = "local"
    tier = ToolTier.LOCAL
    cost_per_call = 0.0
    description = "Generate PowerPoint slides from structured slide deck data"
    agent_skills = []

    def execute(self, **kwargs) -> ToolResult:
        """Build a PPTX file from slide data.

        Args:
            slides: list of dicts with title, content_points, speaker_notes
            output_path: where to save the .pptx file
            module_title: title for the title slide
        """
        slides = kwargs.get("slides", [])
        output_path = kwargs.get("output_path", "output.pptx")
        module_title = kwargs.get("module_title", "Untitled")

        if not slides:
            return ToolResult(success=False, error="No slides provided")

        try:
            from pptx import Presentation
            from pptx.util import Inches, Pt

            prs = Presentation()

            for slide_data in slides:
                # Use blank layout for flexibility
                slide_layout = prs.slide_layouts[1]  # Title and Content
                slide = prs.slides.add_slide(slide_layout)

                # Title
                title = slide.shapes.title
                if title:
                    title.text = slide_data.get("title", "")

                # Content points
                content = slide.placeholders[1] if len(slide.placeholders) > 1 else None
                if content:
                    tf = content.text_frame
                    for i, point in enumerate(slide_data.get("content_points", [])):
                        if i == 0:
                            tf.text = point
                        else:
                            p = tf.add_paragraph()
                            p.text = point

                # Speaker notes
                notes_slide = slide.notes_slide
                notes_slide.notes_text_frame.text = slide_data.get("speaker_notes", "")

            prs.save(output_path)
            return ToolResult(
                success=True,
                data={"output_path": output_path, "slide_count": len(slides)},
            )
        except ImportError:
            return ToolResult(success=False, error="python-pptx not installed")
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def get_status(self) -> ToolStatus:
        try:
            import pptx
            return ToolStatus.AVAILABLE
        except ImportError:
            return ToolStatus.UNAVAILABLE
