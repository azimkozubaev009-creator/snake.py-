import os
import cv2
import threading
import numpy as np
from flask import Flask, render_template, Response, url_for

import matplotlib
matplotlib.use('Agg') 

from game import SnakeGameAI
from agent import Agent, save_plot

app = Flask(__name__)

output_frame = None
lock = threading.Lock()
scores = []
mean_scores = []
total_score = 0

def train_loop():
    global output_frame, total_score, scores, mean_scores
    # headless=True для корректной работы внутри Flask
    game = SnakeGameAI(headless=True)
    agent = Agent()
    
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        # Конвертация кадра Pygame для стрима
        import pygame
        img_data = pygame.surfarray.array3d(game.display)
        img_data = img_data.transpose([1, 0, 2])
        img_bgr = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
        
        with lock:
            output_frame = img_bgr.copy()

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            total_score += score
            scores.append(total_score)
            mean_scores.append(total_score / agent.n_games)
            save_plot(scores, mean_scores)

def generate_frames():
    while True:
        with lock:
            if output_frame is None: continue
            res, buffer = cv2.imencode('.jpg', output_frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    import pygame
    if not os.path.exists('static'): os.makedirs('static')
    threading.Thread(target=train_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
