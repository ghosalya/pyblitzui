# #!/usr/bin/env python

import os
from pyblitzui.app_server import BlitzApp

if __name__ == "__main__":
    script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "simple_ui.py"
    )
    app = BlitzApp(script_path)
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)
