from flask import Flask, jsonify, request, redirect
from youtube_transcript_api import YouTubeTranscriptApi
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['FLASK_ENV'] = 'production'

app = Flask(__name__)
    
@app.route('/api/yt-trans', methods=['GET'])
def get_transcript():
    
    video_id = request.args.get('video_id')
    secret = request.args.get('secret')

    if not (video_id and secret):
        return redirect('https://www.genelify.com')

    if secret != 'e2312da35135dfcd690faaaf3510977f':
        return redirect('https://www.genelify.com')
    
    try:

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        lang = ''
        transcript_result = []

        for transcript in transcript_list:

            if transcript.is_generated:
                
                lang = transcript.language_code

            else:

                lang = transcript.language_code
    
        if lang:
            transcript_result = transcript_list.find_transcript([lang]).fetch()

        if transcript_result:
            status = True
        else:
            status = False

        return jsonify({'success': status, 'video_lang_code': lang, 'transcript': transcript_result})
        
    except Exception as e:
        
        return jsonify({'success': False, 'video_lang_code': '', 'transcript': [], 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)