import os
import datetime
from .style_generator import StyleGenerator


class HTMLGenerator:
    @staticmethod
    def generate_home_status(home, output_dir="_site"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        StyleGenerator.generate_css(output_dir)

        with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
            f.write(
                f"""<!DOCTYPE html>
<html>
<head>
    <title>Slimme Woning</title>
    <meta http-equiv="refresh" content="5">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>Slimme Woning</h1>
    </div>
    <div class="main-content">
        <div class="container">
            <div class="tijdstip">Laatst bijgewerkt: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M %p')}</div>
"""
            )

            for kamer in home.kamers:
                f.write(f'<div class="kamer">\n')
                f.write(f"<h2>{kamer.name}</h2>\n")

                if hasattr(kamer, "bewoners") and kamer.bewoners:
                    f.write('<div class="bewoners">👤 Bewoners: ')
                    f.write(", ".join([bewoner.name for bewoner in kamer.bewoners]))
                    f.write("</div>\n")
                else:
                    f.write('<div class="bewoners leeg">Kamer is leeg</div>\n')

                f.write("<h3>Apparaten:</h3>\n")
                for apparaat in kamer.apparatten:
                    f.write(
                        f'<div class="apparaat">{apparaat.name}: {apparaat.get_status()}</div>\n'
                    )
                f.write("</div>\n")

            f.write("</div>\n")

            f.write('<div class="logger-section">\n')
            f.write("<h2>Logger</h2>\n")
            for log_entry in reversed(
                home.logger.get_recent_messages()[-10:]
            ):  # Toon alleen laatste 10 berichten
                timestamp = log_entry[1:20]
                message = log_entry[22:]
                f.write(f'<div class="log-entry">\n')
                f.write(f'<div class="timestamp">{timestamp}</div>\n')
                f.write(f"{message}\n")
                f.write("</div>\n")
            f.write("</div>\n")

            f.write("</div>\n")
            f.write(
                """
</body>
</html>
"""
            )
        return f"HTML statuspagina en stijl gegenereerd in {output_dir}/index.html en style.css"

    @staticmethod
    def genereer_woning_status(woning, output_dir="_site"):
        return HTMLGenerator.generate_home_status(woning, output_dir)
