import os
import tempfile

from js import sendFile

# A shim to decorate MPL Figure object, so .show() and .savefig() forward it to console
class MPLShim:
    def __init__(self, fig):
      self.fig = fig

    def show(self, warn=True):
        self.savefig("figure.svg")

    def savefig(self, fname, *, transparent=None, dpi='figure', format=None,
        metadata=None, bbox_inches=None, pad_inches=0.1,
        facecolor='auto', edgecolor='auto', backend=None,
        **kwargs
    ):
        # Save to SVG
        with tempfile.NamedTemporaryFile(delete_on_close=False) as svgFile:
            self.fig.savefig(
                svgFile.name,
                transparent=transparent,
                dpi=dpi,
                format="svg",
                metadata=metadata,
                bbox_inches=bbox_inches,
                pad_inches=pad_inches,
                facecolor=facecolor,
                edgecolor=edgecolor,
            )
            with open(svgFile.name, mode="rb") as f:
                svgData = f.read()

        fnameRaw, fnameExt = os.path.splitext(fname)
        if fnameExt == ".svg":
            sendFile(fname, "image/svg+xml", svgData)
        else:
            # Guess the content type / format from an extension
            outDataContentType = None
            outDataFormat = None
            # Those are types MPL supports
            match fnameExt:
                case "":
                    outDataContentType = "image/png"
                    outDataFormat = "png"
                    fname += ".png"
                case ".png":
                    outDataContentType = "image/png"
                    outDataFormat = "png"
                case ".pdf":
                    outDataContentType = "application/pdf"
                    outDataFormat = "pdf"
                case ".ps":
                    outDataContentType = "application/postscript"
                    outDataFormat = "ps"
            if outDataContentType is None:
                # If the format is not supported by MPL, don't ask it to produce empty output
                sendFile(fnameRaw + ".svg", "image/svg+xml", svgData)
            else:
                # Some valid non-SVG output format got requested; as temporary file name
                # provides no MPL-recognizable extension, pass format explicitly
                with tempfile.NamedTemporaryFile(delete_on_close=False) as outFile:
                    self.fig.savefig(
                        outFile.name,
                        transparent=transparent,
                        dpi=dpi,
                        format=outDataFormat,
                        metadata=metadata,
                        bbox_inches=bbox_inches,
                        pad_inches=pad_inches,
                        facecolor=facecolor,
                        edgecolor=edgecolor,
                    )
                    with open(outFile.name, mode="rb") as f:
                        outData = f.read()
                sendFile(fname, "image/svg+xml", svgData, outDataContentType, outData)
