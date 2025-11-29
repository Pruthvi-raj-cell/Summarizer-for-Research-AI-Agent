
import json
import os

class ReportBuilder:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def compile_report(self, filename: str, metadata: dict, chunk_summaries: list) -> str:
        report = f"# Summary: {metadata.get('title', filename)}\n\n"
        
        for item in chunk_summaries:
            report += f"## {item.get('section_guess', 'Section')}\n"
            for point in item.get('summary_points', []):
                report += f"- {point}\n"
            report += "\n"

        out_path = os.path.join(self.output_dir, f"{filename}_summary.md")
        with open(out_path, "w") as f:
            f.write(report)
        return out_path
