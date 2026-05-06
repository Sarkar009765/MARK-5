import os
import sys
import threading
import webbrowser
from flask import Flask, request, jsonify, render_template
from utils import logger, get_resource_path
from memory.db import memory

class WebUI:
    def __init__(self, brain):
        self.brain = brain
        
        # In PyInstaller, templates folder is bundled. We need correct path.
        template_dir = get_resource_path('templates')
        self.app = Flask(__name__, template_folder=template_dir, static_folder=template_dir)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            data = request.json
            if not data or 'message' not in data:
                return jsonify({"error": "No message provided"}), 400
            
            user_input = data['message']
            try:
                # Process the message through the ClawVis brain
                response = self.brain.process(user_input)
                
                # Speak it if TTS is running, but let's just do text for UI to be safe
                # We can trigger voice optionally.
                from voice.tts import tts
                tts.speak_async(response)
                
                return jsonify({"response": response})
            except Exception as e:
                logger.error(f"Web UI Chat Error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route('/api/history', methods=['GET'])
        def history():
            try:
                # Get last 20 messages for UI
                conversations = memory.get_conversations(20)
                # Filter out system logs if needed, just return role and content
                history = [{"role": msg["role"], "content": msg["content"]} for msg in conversations]
                return jsonify({"history": history})
            except Exception as e:
                logger.error(f"Web UI History Error: {e}")
                return jsonify({"error": str(e)}), 500

    def run(self):
        # Disable Flask default logging to not clutter the console
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        logger.info("Starting Web UI on http://127.0.0.1:5000")
        self.app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def start_web_ui(brain, auto_open=True):
    ui = WebUI(brain)
    thread = threading.Thread(target=ui.run, daemon=True)
    thread.start()
    
    if auto_open:
        # Give it a second to start
        import time
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:5000")
