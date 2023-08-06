"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/stories')
def stories_list():
    return render_template(
        'stories/stories.html',
        title='Stories',
    )

@app.route('/stories/create')
def stories_create():
    return render_template(
        'stories/story.html',
        title='Story',
        model={'name': '', 'text': ''},
        model_json=json.dumps({'name': '', 'text': ''})
    )

@app.route('/stories/edit/<name>', methods=['GET'])
def stories_edit(name):
    story = StoriesService().get_by_name(name)
    return render_template(
        'stories/story.html',
        title='Story',
        model=story,
        model_json=json.dumps(story)
    )

@app.route('/api/stories', methods=['GET'])
def api_stories_list():
    q = request.args.get('q')
    stories = StoriesService().find_all(q)
    return jsonify(stories)

@app.route('/api/stories/<name>', methods=['GET'])
def api_stories_get(name):
    story = StoriesService().get_by_name(name)
    return jsonify(story)

@app.route('/api/stories/<name>', methods=['POST'])
def api_stories_post(name):
    updated_story = request.json
    if name.lower() != updated_story['name'].lower():
        existing_story = StoriesService().get_by_name(updated_story['name'].lower())
        if existing_story:
            return jsonify({'error': 'Story with the name already exits.'})
    
    StoriesService().update(name, updated_story)
    return jsonify({'result': updated_story})

@app.route('/api/stories/<name>', methods=['PUT'])
def api_stories_put(name):
    existing_story = StoriesService().get_by_name(name)
    if existing_story:
        return jsonify({'error': 'Story with the name already exits.'})

    new_story = request.json
    StoriesService().update(name, new_story)
    return jsonify({'result': new_story})

@app.route('/api/stories/<name>', methods=['DELETE'])
def api_stories_delete(name):
    StoriesService().delete(name)
    return jsonify({'result': 'ok'})