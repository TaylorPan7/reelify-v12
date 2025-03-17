from flask import render_template, request, jsonify, send_from_directory, redirect, url_for, session, flash
import os
import json
import time
import random
import asyncio
from auth import user_exists, register_user, authenticate, get_user
from video_generator import run_video_generation, video_progress

def register_routes(app):
    @app.route('/')
    def index():
        if 'email' in session:
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            if user_exists(email):
                flash('Email already registered')
                return redirect(url_for('signup'))
            
            register_user(email, password)
            flash('Account created successfully! Please login.')
            return redirect(url_for('login'))
        
        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            if authenticate(email, password):
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password')
        
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        if 'email' not in session:
            return redirect(url_for('login'))
        
        user = get_user(session['email'])
        return render_template('dashboard.html', user=user)

    @app.route('/logout')
    def logout():
        session.pop('email', None)
        return redirect(url_for('index'))

    @app.route('/socials')
    def socials():
        return render_template('socials.html')

    @app.route('/video-generator')
    def video_generator():
        return render_template('video_generator.html')

    @app.route('/image-generator')
    def image_generator():
        return render_template('image_generator.html')

    @app.route('/captioner')
    def captioner():
        return render_template('captioner.html')

    @app.route('/pricing')
    def pricing():
        return render_template('pricing.html')

    # Company pages
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/careers')
    def careers():
        return render_template('careers.html')

    @app.route('/press')
    def press():
        return render_template('press.html')

    @app.route('/partners')
    def partners():
        return render_template('partners.html')

    # Resources pages
    @app.route('/blog')
    def blog():
        return render_template('blog.html')

    @app.route('/tutorials')
    def tutorials():
        return render_template('tutorials.html')

    @app.route('/support')
    def support():
        return render_template('support.html')

    @app.route('/api-docs')
    def api_docs():
        return render_template('api_docs.html')

    # Legal pages
    @app.route('/terms')
    def terms():
        return render_template('terms.html')

    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/cookies')
    def cookies():
        return render_template('cookies.html')

    @app.route('/gdpr')
    def gdpr():
        return render_template('gdpr.html')

    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)

    @app.route('/video/<path:filename>')
    def serve_video(filename):
        return send_from_directory('.', filename)

    @app.route('/output/<path:filename>')
    def serve_output(filename):
        return send_from_directory('.', filename)

    @app.route('/generate-video', methods=['POST'])
    def generate_video():
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            topic = data.get('topic')
            if not topic:
                return jsonify({'error': 'Topic is required'}), 400
            
            # Generate a unique ID for this video
            video_id = f"{int(time.time())}_{random.randint(1000, 9999)}"
            
            try:
                # Start the async video generation
                asyncio.run(run_video_generation(topic, video_id))
                
                return jsonify({
                    'success': True,
                    'video_id': video_id,
                    'message': 'Video generation started'
                })
            except Exception as e:
                # Log the error for debugging
                print(f"Error in video generation process: {str(e)}")
                return jsonify({
                    'error': f'Failed to start video generation: {str(e)}'
                }), 500
                
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({'error': 'Invalid request format'}), 400

    @app.route('/check-video-status/<video_id>')
    def check_video_status(video_id):
        try:
            if video_id not in video_progress:
                return jsonify({
                    'status': 'not_found',
                    'error': 'Video generation not found'
                }), 404

            progress = video_progress[video_id]
            
            # If the video is completed, clean up the progress data
            if progress['status'] == 'completed':
                response_data = progress.copy()
                del video_progress[video_id]  # Clean up progress data
                return jsonify(response_data)
                
            return jsonify(progress)
            
        except Exception as e:
            print(f"Error checking video status: {str(e)}")
            return jsonify({
                'status': 'error',
                'error': f'Failed to check video status: {str(e)}'
            }), 500

    @app.route('/generate-image', methods=['POST'])
    def generate_image():
        # Placeholder for image generation
        try:
            data = request.json
            prompt = data.get('prompt')
            
            if not prompt:
                return jsonify({'error': 'Prompt is required'}), 400
            
            # In a real implementation, this would call an image generation API
            # For now, we'll simulate this step
            
            # Return a placeholder image URL
            return jsonify({
                'success': True,
                'image_url': '/static/sample-image.jpg',
                'message': 'Image generated successfully'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/generate-captions', methods=['POST'])
    def generate_captions():
        # Placeholder for caption generation
        try:
            # In a real implementation, this would process the uploaded video
            # and generate captions
            
            # Return placeholder data
            return jsonify({
                'success': True,
                'captions': [
                    {'start': '00:00:02', 'end': '00:00:05', 'text': 'This is a sample caption.'},
                    {'start': '00:00:06', 'end': '00:00:09', 'text': 'Generated automatically by our system.'},
                    {'start': '00:00:10', 'end': '00:00:14', 'text': 'You can download the captioned video below.'}
                ],
                'video_url': '/sample-captioned-video.mp4',
                'srt_url': '/sample-captions.srt',
                'message': 'Captions generated successfully'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500 