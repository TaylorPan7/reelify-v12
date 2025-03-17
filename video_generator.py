import os
import time
import subprocess
import asyncio

# Store video generation progress
video_progress = {}

async def run_video_generation(topic, video_id):
    try:
        # Initialize progress
        video_progress[video_id] = {
            'status': 'starting',
            'progress': 0,
            'current_step': 'Initializing...',
            'error': None
        }

        def update_progress(progress, step):
            print(f"Progress update: {progress}% - {step}")  # Debug logging
            video_progress[video_id] = {
                'status': 'in_progress',
                'progress': progress,
                'current_step': step,
                'error': None
            }

        # Step 1: Run pexels_maker.py (40%)
        update_progress(5, 'Generating script and downloading videos...')
        
        # Create a process to run pexels_maker.py and pipe the topic
        process = subprocess.Popen(
            ['python', 'pexels_maker.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the topic to the script
        stdout, stderr = process.communicate(input=f"{topic}\n")
        
        if process.returncode != 0:
            raise Exception(f"Failed to generate video: {stderr}")
        
        print("pexels_maker.py completed successfully")
        update_progress(40, 'Videos downloaded and combined')

        # Step 2: Run merge.py (60%)
        update_progress(45, 'Merging video and audio...')
        try:
            result = subprocess.run(['python', 'merge.py'], check=True, capture_output=True, text=True)
            print("merge.py output:", result.stdout)
            if result.stderr:
                print("merge.py stderr:", result.stderr)
            
            # Wait for the file to be created and check its existence
            time.sleep(2)  # Give some time for file operations to complete
            if not os.path.exists('final_video_output.mp4'):
                raise Exception("merge.py did not create final_video_output.mp4")
            
            update_progress(60, 'Video and audio merged')
        except subprocess.CalledProcessError as e:
            print(f"Error in merge.py: {e.stdout}\n{e.stderr}")
            raise Exception(f"Failed to merge video and audio: {e.stderr}")

        # Step 3: Run transcriber_script.py (80%)
        update_progress(65, 'Generating transcription...')
        try:
            # Check input file exists
            if not os.path.exists('final_video_output.mp4'):
                raise Exception("Input video file not found before transcription")
            
            result = subprocess.run(['python', 'transcriber_script.py'], check=True, capture_output=True, text=True)
            print("transcriber_script.py output:", result.stdout)
            if result.stderr:
                print("transcriber_script.py stderr:", result.stderr)
            
            # Wait for the file to be created and check its existence
            time.sleep(2)  # Give some time for file operations to complete
            if not os.path.exists('output_captions.srt'):
                raise Exception("transcriber_script.py did not create output_captions.srt")
            
            update_progress(80, 'Transcription generated')
        except subprocess.CalledProcessError as e:
            print(f"Error in transcriber_script.py: {e.stdout}\n{e.stderr}")
            raise Exception(f"Failed to generate transcription: {e.stderr}")

        # Step 4: Run captioned_video.py (100%)
        update_progress(85, 'Adding captions...')
        try:
            # Check input files exist
            if not os.path.exists('final_video_output.mp4'):
                raise Exception("Input video file not found before captioning")
            if not os.path.exists('output_captions.srt'):
                raise Exception("Input SRT file not found before captioning")
            
            result = subprocess.run(['python', 'captioned_video.py'], check=True, capture_output=True, text=True)
            print("captioned_video.py output:", result.stdout)
            if result.stderr:
                print("captioned_video.py stderr:", result.stderr)
            
            # Wait for the file to be created and check its existence
            time.sleep(2)  # Give some time for file operations to complete
            if not os.path.exists('captioned_video.mp4'):
                raise Exception("captioned_video.py did not create captioned_video.mp4")
            
        except subprocess.CalledProcessError as e:
            print(f"Error in captioned_video.py: {e.stdout}\n{e.stderr}")
            raise Exception(f"Failed to add captions: {e.stderr}")

        # Rename files with video_id prefix to avoid conflicts
        final_video_name = f"{video_id}_final_video.mp4"
        srt_file_name = f"{video_id}_captions.srt"

        if not os.path.exists('captioned_video.mp4'):
            raise Exception(f"Final video file not found: captioned_video.mp4")
        if not os.path.exists('output_captions.srt'):
            raise Exception(f"SRT file not found: output_captions.srt")

        # Rename the files
        os.rename('captioned_video.mp4', final_video_name)
        os.rename('output_captions.srt', srt_file_name)

        # Update final status
        video_progress[video_id] = {
            'status': 'completed',
            'progress': 100,
            'current_step': 'Video generation completed!',
            'error': None,
            'video_url': f'/video/{final_video_name}',
            'srt_url': f'/video/{srt_file_name}'
        }
        print("Video generation completed successfully")

    except Exception as e:
        error_message = str(e)
        print(f"Error generating video: {error_message}")
        video_progress[video_id] = {
            'status': 'error',
            'progress': 0,
            'current_step': 'Error occurred',
            'error': error_message
        } 