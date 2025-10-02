"""Packagemaxxing: Scanner Art AI Camera
Minimal code, maximum AI/visual effects leverage on Apple Silicon
"""
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("🚀 Starting Packagemaxxing...")

import gradio as gr
import numpy as np
import cv2
from collections import deque
import random

logger.info("✓ All dependencies loaded")

# Global state
scanner_buffer = deque(maxlen=100)
gallery_items = []
frame_count = 0

# VISUAL EFFECTS
def apply_scanlines(img, line_height=4):
    h, w = img.shape[:2]
    for y in range(0, h, line_height * 2):
        img[y:y+line_height] = (img[y:y+line_height] * 0.3).astype(np.uint8)
    return img

def overlay_matrix(img, density=50):
    h, w = img.shape[:2]
    overlay = img.copy()
    for _ in range(density):
        x = random.randint(0, w-20)
        y = random.randint(10, h-10)
        cv2.putText(overlay, random.choice('01アイウエオカキ'), (x, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 65), 1)
    return cv2.addWeighted(img, 0.7, overlay, 0.3, 0)

def apply_posterize(img, levels=4):
    indices = np.arange(0, 256)
    divider = np.linspace(0, 255, levels + 1)[1]
    quantiz = np.int0(np.linspace(0, 255, levels))
    color_levels = np.clip(np.int0(indices / divider), 0, levels - 1)
    palette = quantiz[color_levels]
    return palette[img]

def apply_glitch(img, intensity=10):
    offset = random.randint(-intensity, intensity)
    glitched = img.copy()
    if len(img.shape) == 3 and img.shape[2] == 3:
        glitched[:, :, 0] = np.roll(img[:, :, 0], offset, axis=1)
        glitched[:, :, 2] = np.roll(img[:, :, 2], -offset, axis=1)
    return glitched

# RENDERING
def add_to_scanner_buffer(frame):
    if frame is not None and len(frame.shape) >= 2:
        h = frame.shape[0]
        mid_line = frame[h//2:h//2+2]
        scanner_buffer.append(mid_line)

def render_scanner_art():
    if len(scanner_buffer) == 0:
        return np.zeros((480, 640, 3), dtype=np.uint8)
    stacked = np.vstack(list(scanner_buffer))
    return cv2.resize(stacked, (640, 480))

def create_storyboard_frame(frame, label=""):
    if frame is None:
        return np.zeros((480, 640, 3), dtype=np.uint8)
    panel = cv2.resize(frame, (300, 225))
    bordered = cv2.copyMakeBorder(panel, 10, 40, 10, 10,
                                 cv2.BORDER_CONSTANT, value=(0, 255, 65))
    cv2.putText(bordered, label[:30], (15, panel.shape[0] + 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return bordered

# MAIN PROCESSING
def process_frame(image, mode, effects):
    global frame_count
    frame_count += 1
    
    if image is None:
        logger.warning("⚠️ No image received from webcam")
        return None
    
    logger.info(f"✓ Processing frame {frame_count}")
    
    # Ensure numpy array and RGB
    frame = np.array(image)
    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    elif frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    
    # Apply effects
    if effects:
        if 'scanlines' in effects:
            frame = apply_scanlines(frame)
        if 'matrix_rain' in effects:
            frame = overlay_matrix(frame)
        if 'posterize' in effects:
            frame = apply_posterize(frame)
        if 'glitch' in effects:
            frame = apply_glitch(frame)
    
    # Render
    if mode == 'Scanner Art':
        add_to_scanner_buffer(frame)
        output = render_scanner_art()
    else:
        label = f"Frame {frame_count}"
        output = create_storyboard_frame(frame, label)
    
    return output

def save_to_gallery(image):
    if image is not None:
        gallery_items.append(image)
        logger.info(f"💾 Gallery: {len(gallery_items)} items")
        return gallery_items[-10:]
    return []

# INTERFACE
logger.info("🎨 Building interface...")

with gr.Blocks(css="body { background: #0a0e1b; color: #00ff41; }") as demo:
    
    gr.Markdown("# 🎨 Packagemaxxing: Scanner Art AI Camera")
    
    with gr.Row():
        with gr.Column():
            # Use type="numpy" and remove streaming for better compatibility
            camera = gr.Image(
                sources=['webcam'],
                type="numpy",
                label="📷 Live Feed"
            )
            
            mode = gr.Radio(
                choices=['Scanner Art', 'Storyboard'],
                value='Scanner Art',
                label="🎭 Mode"
            )
            
            effects = gr.CheckboxGroup(
                choices=['scanlines', 'matrix_rain', 'posterize', 'glitch'],
                value=['scanlines'],
                label="✨ Effects"
            )
            
            process_btn = gr.Button("🎨 Process Frame", variant="primary")
            save_btn = gr.Button("💾 Save to Gallery")
        
        with gr.Column():
            output = gr.Image(label="🖼️ Output")
            gallery = gr.Gallery(label="📸 Gallery", columns=3, height=400)
    
    gr.Markdown("""
    ### 🎯 Usage
    1. Click webcam preview to capture a frame
    2. Click "Process Frame" to apply effects
    3. Click "Save to Gallery" to keep it
    
    *Tip: In Scanner Art mode, process multiple frames to build up the effect*
    """)
    
    # Wire up events
    process_btn.click(
        fn=process_frame,
        inputs=[camera, mode, effects],
        outputs=output
    )
    
    save_btn.click(
        fn=save_to_gallery,
        inputs=output,
        outputs=gallery
    )

logger.info("✅ Ready to launch")

if __name__ == "__main__":
    logger.info("⚠️ Open http://127.0.0.1:7860 in your browser")
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )