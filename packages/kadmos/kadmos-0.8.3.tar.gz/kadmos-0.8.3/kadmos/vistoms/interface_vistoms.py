import ast
import fnmatch
import json
import logging
import os
import shutil
import sys
import tempfile
import time
import uuid
import zipfile
from copy import deepcopy
from shutil import copyfile

import networkx as nx
from flask import Flask, request, render_template, jsonify
from kadmos.cmdows.cmdows import find_cmdows_file
from kadmos.graph import load, FundamentalProblemGraph

# Folder and file settings
UPLOAD_FOLDERS = dict()
TEMP_FILE = 'tmp'


def interface(debug=True, tempdir=None):

    # Initial settings
    app = Flask(__name__)
    if debug:
        app.debug = True
    if tempdir:
        tempfile.tempdir = tempdir

    # Index
    @app.route("/")
    def index(error=None, message=None, selection=False):
        # Check if error or message is send
        if request.values.get('error', False) and error is None:
            error = request.values['error']
        if request.values.get('message', False) and message is None:
            message = request.values['message']
        # Render index
        return render_template('index.html', error=error, message=message, selection=selection, page='start')

    # Start the empty vistoms app
    @app.route('/startnewvistoms')
    def start_new_vistoms(error=None, message=None):

        # Check if error or message is send
        if request.values.get('error', False) and error is None:
            error = request.values['error']
        if request.values.get('message', False) and message is None:
            message = request.values['message']
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

        # Get random uuid for session
        session_id = str(uuid.uuid4())

        # Create temporary directory and its mapping with the session ID in the global variable
        UPLOAD_FOLDERS[session_id] = tempfile.mkdtemp()

        # Wait for directory to exist
        attempts = 0
        while True:
            if os.path.isdir(UPLOAD_FOLDERS[session_id]):
                break
            time.sleep(1)
            attempts += 1
            if attempts > 20:
                raise ReferenceError('Could not create new temporary directory.')

        return render_template('VISTOMS_sessions.html', new=0, error=error, message=message, sessionID=session_id)

    # Start the populated vistoms app
    @app.route('/startpopulatedvistoms')
    def start_populated_vistoms(error=None, message=None):

        # Check if error or message is send
        if request.values.get('error', False) and error is None:
            error = request.values['error']
        if request.values.get('message', False) and message is None:
            message = request.values['message']
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

        # Get random uuid for session
        session_id = str(uuid.uuid4())

        # Create temporary directory and its mapping with the session ID in the global variable
        UPLOAD_FOLDERS[session_id] = tempfile.mkdtemp()

        # Wait for directory to exist
        attempts = 0
        while True:
            if os.path.isdir(UPLOAD_FOLDERS[session_id]):
                break
            time.sleep(1)
            attempts += 1
            if attempts > 20:
                raise ReferenceError('Could not create new temporary directory.')

        # Copy all files from folder to another folder
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'examples')
        src_files = os.listdir(folder)
        for file_name in src_files:
            full_file_name = os.path.join(folder, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, UPLOAD_FOLDERS[session_id])

        return render_template('VISTOMS_sessions.html', new=0, error=error, message=message, sessionID=session_id)

    # Info
    @app.route('/info')
    def info():
        return render_template('info.html', page='info')

    # Acknowledgements
    @app.route('/acknowledgements')
    def acknowledgements():
        return render_template('acknowledgements.html', page='acknowledgements')

    @app.route('/kadmos_upload_file', methods=['GET', 'POST'])
    def kadmos_upload_file():
        """
            Function uploads a file to the temp folder and returns the graph information to VISTOMS

            :return: VISTOMS json data with graph information
        """
        try:
            if request.method == 'POST':
                # get request form
                fileType = request.form['fileType']
                newGraphID = request.form['newGraphID']
                sessionID = request.form['sessionID']
                uploaded_files = request.files.getlist("file[]")

                number_of_files = len(uploaded_files)
                if number_of_files > 2:
                    return ("ERROR: Max. number of files that can be uploaded is 2!")

                mpgFile = []
                dgFile = []
                for file in uploaded_files:
                    if "_mpg" in file.filename:
                        mpgFile = file
                    else:
                        dgFile = file

                # check if the post request has the file part
                if 'file[]' not in request.files:
                    return ("ERROR: No file part!")

                # if user does not select file, browser also
                # submit a empty part without filename
                if dgFile.filename == '':
                    return ("ERROR: No file part!")
                if dgFile:
                    # Check if the right filetypes were chosen
                    if fileType == 'CMDOWS file' and dgFile.filename.rsplit('.', 1)[1].lower() != "xml":
                        return ("ERROR: Wrong file type! Please use a valid CMDOWS file")
                    elif fileType == 'KDMS file(s)' and dgFile.filename.rsplit('.', 1)[1].lower() != "kdms":
                        return ("ERROR: Wrong file type! Please use a valid KDMS file")
                    elif fileType == 'Database' and dgFile.filename.rsplit('.', 1)[1].lower() != "zip":
                        return ("ERROR: Wrong file type! Please use a valid zip file")

                    upload_folder = UPLOAD_FOLDERS[sessionID]
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)

                database_dir = ""
                if fileType == 'Database':
                    database_dir = os.path.join(upload_folder, 'database_tmp')
                    zip_ref = zipfile.ZipFile(file, 'r')
                    zip_ref.extractall(database_dir)
                    zip_ref.close()
                    file_list = []
                    database_listdir = os.listdir(database_dir)

                    # Handle case where the database is stored as a subfolder in de zip archive (as done on MacOS)
                    actual_database_dir = database_dir
                    if len(database_listdir) == 1 or '__MACOSX' in database_listdir:
                        if '__MACOSX' in database_listdir:
                            database_listdir.remove('__MACOSX')
                        if os.path.isdir(os.path.join(database_dir, database_listdir[0])):
                            actual_database_dir = os.path.join(database_dir, database_listdir[0])
                    for file in os.listdir(actual_database_dir):
                        file_list.append(os.path.join(actual_database_dir, file))
                    cmdows_file = find_cmdows_file(file_list)
                    graphFileName = cmdows_file
                else:
                    graphFileName = os.path.join(upload_folder, dgFile.filename)
                    dgFile.save(os.path.join(upload_folder, dgFile.filename))

                loaded_graph = load(graphFileName, file_check_critical=False)
                if "name" not in loaded_graph.graph:
                    loaded_graph.graph["name"] = os.path.splitext(dgFile.filename)[0].replace("_",".")
                    # Remove the uploaded file (and if existing, database directory) from the temp folder
                    os.remove(graphFileName)
                    if os.path.exists(database_dir):
                        shutil.rmtree(database_dir)

                    if isinstance(loaded_graph, tuple):
                        graph = loaded_graph[0]
                        mpg = loaded_graph[1]
                    elif mpgFile:
                        # Check if the right filetype was chosen
                        if mpgFile.filename.rsplit('.', 1)[1].lower() != "kdms":
                            return ("ERROR: Wrong file type! Please use a valid KDMS file")
                        graph = loaded_graph
                        mpgFileName = mpgFile.filename
                        mpgFile.save(os.path.join(upload_folder, mpgFileName))
                        mpg = load(os.path.join(upload_folder, mpgFileName), file_check_critical=True)
                        # Remove the uploaded file from the temp folder
                        os.remove(os.path.join(upload_folder, mpgFileName))
                    else:
                        graph = loaded_graph
                        mpg = None

                    # save the graph as kdms file in temp folder
                    graph.save(os.path.join(upload_folder, TEMP_FILE + '_' + newGraphID + '.kdms'), file_type='kdms',
                               graph_check_critical=False, mpg=mpg)

                    # Use function order for VISTOMS if it is available in the graph information
                    function_order = None
                    if graph.graph_has_nested_attributes('problem_formulation', 'function_order') and mpg == None:
                        function_order = graph.graph['problem_formulation']['function_order']

                    # Add the graph with the updated function order to VISTOMS
                    newVistomsData = graph.vistoms_add_json(graph_id=newGraphID, function_order=function_order, mpg=mpg)

                    return newVistomsData

            return ("ERROR: File type " + dgFile.filename.rsplit('.', 1)[1].lower() + " not allowed!")

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.


    @app.route('/kadmos_create_new_graph', methods=['POST'])
    def kadmos_create_new_graph():
        try:
            # Get request form
            graph_name = request.form['graph_name']
            graph_description = request.form['graph_description']
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Open cmdows template file and load it as graph
            cmdows_template = os.path.join('templates', 'cmdows_template.xml')
            graph_template = load(cmdows_template, check_list=['consistent_root', 'invalid_leaf_elements'])

            # Determine graph_id
            graph_ids = []
            for aFile in os.listdir(upload_folder):
                if aFile.endswith('.kdms'):
                    filename = aFile.split('.kdms')[0]
                    graph_ids.append(int(filename.split('_')[1]))
            graph_id_int = max(graph_ids)+1
            graph_id = format(graph_id_int, "02")

            # Allocate graph name, description and id
            graph_template.graph['name'] = graph_name
            graph_template.graph['description'] = graph_description
            graph_template.graph['id'] = graph_id

            # Delete dummy design competence
            graph_template.remove_node('dummy')

            # Save empty graph as kdms file
            graph_template.save(os.path.join(upload_folder, 'tmp_'+graph_id+'.kdms'), file_type='kdms', graph_check_critical=False, mpg=None)

            # Add graph to vistoms data
            newVistomsData = graph_template.vistoms_add_json(mpg=None, graph_id=graph_id)

            return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.


    @app.route('/kadmos_export_all_graphs', methods=['POST'])
    def kadmos_export_all_graphs():
        """
           Function exports all graphs to a folder as CMDOWS or KDMS files

           :param path: the path of the folder, the files are exported to
           :return: path
        """
        try:
            # Get request form
            path = os.path.join(request.form['path'], '')
            fileType = request.form['fileType']
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            if not os.path.isdir(path):
                os.makedirs(os.path.dirname(path))

            for aFile in os.listdir(upload_folder):
                if aFile.endswith(".kdms"):
                    fileName = aFile.split('.')[0]
                    fileName_split = fileName.split('_')
                    if "mpg" not in fileName_split and "backup" not in fileName_split:  # Do not loop through mpg files
                        graphFileName = fileName + ".kdms"
                        mpgFileName = fileName + "_mpg.kdms"
                        if os.path.exists(os.path.join(upload_folder, mpgFileName)):
                            graph = load(os.path.join(upload_folder, graphFileName), file_check_critical=False)
                            mpg = load(os.path.join(upload_folder, mpgFileName), file_check_critical=False)
                        else:
                            graph = load(os.path.join(upload_folder, graphFileName), file_check_critical=False)
                            mpg = None

                        # Add problem function roles if they are not already existing
                        if not hasattr(graph, 'name'):
                            graph_name = fileName
                        else:
                            graph_name = graph.name
                        # Add problem function roles if they are not already existing
                        if isinstance(graph, FundamentalProblemGraph):
                            if 'function_order' not in graph.graph['problem_formulation']:
                                graph.assert_or_add_nested_attribute(['problem_formulation', 'function_order'],
                                                                     None)
                            if 'mdao_architecture' not in graph.graph['problem_formulation']:
                                graph.assert_or_add_nested_attribute(['problem_formulation', 'mdao_architecture'],
                                                                     'undefined')
                            if 'allow_unconverged_couplings' not in graph.graph['problem_formulation']:
                                graph.assert_or_add_nested_attribute(
                                    ['problem_formulation', 'allow_unconverged_couplings'],
                                    False)
                            graph.add_function_problem_roles()

                        if fileType == "CMDOWS files":
                            file_type = "cmdows"
                            file = graph_name + ".xml"
                            # Save as CMDOWS file
                            graph.save(os.path.join(upload_folder, graph_name), file_type=file_type,
                                       graph_check_critical=False, mpg=mpg)
                            # Copy CMDOWS file from temporary folder to user's download folder
                            copyfile(os.path.join(upload_folder, file), os.path.join(path, file))
                            # remove temporary CMDOWS file
                            os.remove(os.path.join(upload_folder, file))
                        elif fileType == "KDMS files":
                            file_type = "kdms"
                            # Save as kdms file
                            graph.save(os.path.join(upload_folder, graph_name), file_type=file_type,
                                       graph_check_critical=False, mpg=mpg)
                            file = graph_name + ".kdms"
                            mpgfile = graph_name + "_mpg.kdms"
                            # Copy kdms file from temporary folder to user's download folder
                            copyfile(os.path.join(upload_folder, file), os.path.join(path, file))
                            # remove temporary kdms file
                            os.remove(os.path.join(upload_folder, file))
                            if os.path.exists(os.path.join(upload_folder, mpgfile)):
                                copyfile(os.path.join(upload_folder, mpgfile), os.path.join(path, mpgfile))
                                os.remove(os.path.join(upload_folder, mpgfile))
            return path

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_export_graph', methods=['POST'])
    def kadmos_export_graph():
        """
           Function exports the current graph to a CMDOWS or kdms file

           :param file: a CMDOWS or kdms file that goes into the user's download folder
           :return: file
        """
        try:
            # Get request form
            path = os.path.join(request.form['path'], '')
            fileName = request.form['fileName']
            graphID = request.form['graphID']
            fileType = request.form['fileType']
            functionOrder = request.form['currentOrder'].split(',')

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(upload_folder, mpgFileName)):
                graph = load(os.path.join(upload_folder, graphFileName), file_check_critical=False)
                mpg = load(os.path.join(upload_folder, mpgFileName), file_check_critical=False)
            else:
                graph = load(os.path.join(upload_folder, graphFileName), file_check_critical=False)
                mpg = None

            # Add problem function roles if they are not already existing
            if isinstance(graph, FundamentalProblemGraph):
                if 'function_order' not in graph.graph['problem_formulation']:
                    graph.assert_or_add_nested_attribute(['problem_formulation', 'function_order'], None)
                if 'mdao_architecture' not in graph.graph['problem_formulation']:
                    graph.assert_or_add_nested_attribute(['problem_formulation', 'mdao_architecture'], 'undefined')
                if 'allow_unconverged_couplings' not in graph.graph['problem_formulation']:
                    graph.assert_or_add_nested_attribute(['problem_formulation', 'allow_unconverged_couplings'], False)
                graph.add_function_problem_roles()

            if not os.path.isdir(path):
                os.makedirs(os.path.dirname(path))

            if fileType == "kdms":
                copyfile(os.path.join(upload_folder, graphFileName), os.path.join(path, fileName + ".kdms"))
                if os.path.exists(os.path.join(upload_folder, mpgFileName)):
                    copyfile(os.path.join(upload_folder, mpgFileName), os.path.join(path, fileName + '_mpg' + ".kdms"))
            elif fileType == "cmdows":
                file = fileName + ".xml"
                # Save as CMDOWS file
                graph.save(os.path.join(upload_folder, fileName), file_type=fileType, graph_check_critical=False,
                           mpg=mpg)
                # Copy CMDOWS file from temporary folder to user's download folder
                copyfile(os.path.join(upload_folder, file), os.path.join(path, file))
                # remove temporary CMDOWS file
                os.remove(os.path.join(upload_folder, file))
            else:
                return ("ERROR: Wrong file type!!!")

            return (path)

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_save_vistoms_graph', methods=['POST'])
    def kadmos_save_vistoms_graph():
        """
           Function saves current graph as new VISTOMS graph and returns it to the VISTOMS package in the browser

           :return: the graph compressed as VISTOMS data
        """
        try:
            # get request form
            graphID = request.form['graphID']
            newGraphName = request.form['newGraphName']
            newGraphID = request.form['newGraphID']
            function_order = request.form['currentOrder'].split(',')

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            tmpDir = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(tmpDir, mpgFileName)):
                graph = load(os.path.join(tmpDir, graphFileName), file_check_critical=False)
                mpg = load(os.path.join(tmpDir, mpgFileName), file_check_critical=False)
            else:
                graph = load(os.path.join(tmpDir, graphFileName), file_check_critical=False)
                mpg = None

            newFileName = TEMP_FILE + '_' + newGraphID + '.kdms'
            graph.graph['name'] = newGraphName
            graph.save(os.path.join(upload_folder, newFileName), file_type="kdms", graph_check_critical=False, mpg=mpg)

            newVistomsData = graph.vistoms_add_json(function_order=function_order, mpg=mpg, graph_id=newGraphID)

            return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_delete_graph', methods=['POST'])
    def kadmos_delete_graph():
        """
           Function finds all graphs that have been temporarily stored in the temp folder and returns them
           to the VISTOMS package in the browser. This function is always called when the browser is refreshed by the user.

           :return: the graphs compressed as VISTOMS data
        """
        try:
            # get request form
            graphID = request.form['graphID']

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            tmpDir = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            backupGraphFileName = TEMP_FILE + '_' + graphID + '_backup.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            backupMpgFileName = TEMP_FILE + '_' + graphID + '_mpg_backup.kdms'
            if os.path.exists(os.path.join(tmpDir, graphFileName)):
                os.remove(os.path.join(tmpDir, graphFileName))
            if os.path.exists(os.path.join(tmpDir, backupGraphFileName)):
                os.remove(os.path.join(tmpDir, backupGraphFileName))
            if os.path.exists(os.path.join(tmpDir, mpgFileName)):
                os.remove(os.path.join(tmpDir, mpgFileName))
            if os.path.exists(os.path.join(tmpDir, backupMpgFileName)):
                os.remove(os.path.join(tmpDir, backupMpgFileName))

            return kadmos_find_temp_graphs()

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_find_temp_graphs', methods=['POST'])
    def kadmos_find_temp_graphs():
        """
           Function finds all graphs that have been temporarily stored in the temp folder and returns them
           to the VISTOMS package in the browser. This function is always called when the browser is refreshed by the user.

           :return: the graphs compressed as VISTOMS data
        """
        try:
            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # First of all, delete all graphs, that end with a _backup
            delete_backup_graphs()

            tmpDir = upload_folder
            newVIstomsDataArray = []
            file_list = os.listdir(tmpDir)
            if file_list:
                file_list.sort()
            for file in file_list:
                if file.endswith(".kdms"):
                    fileName = file.split('.')[0].split('_')
                    graphID = fileName[1]
                    if "mpg" not in fileName:  # Do not loop through mpg files
                        graphFileName = fileName[0] + "_" + graphID + ".kdms"
                        mpgFileName = fileName[0] + "_" + graphID + "_mpg.kdms"
                        if os.path.exists(os.path.join(tmpDir, mpgFileName)):
                            graph = load(os.path.join(tmpDir, graphFileName), file_check_critical=False)
                            mpg = load(os.path.join(tmpDir, mpgFileName), file_check_critical=False)
                        else:
                            graph = load(os.path.join(tmpDir, graphFileName), file_check_critical=False)
                            mpg = None

                        # Use function order for VISTOMS if it is available in the graph information
                        function_order = None
                        if graph.graph_has_nested_attributes('problem_formulation', 'function_order') and mpg == None:
                            function_order = graph.graph['problem_formulation']['function_order']

                        graph.save(os.path.join(upload_folder, graphFileName), file_type="kdms",
                                   graph_check_critical=False, mpg=mpg)

                        newVIstomsDataArray.append(
                            graph.vistoms_add_json(graph_id=graphID, function_order=function_order,
                                                   mpg=mpg))

            return jsonify(newVIstomsDataArray)

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_revert_step', methods=['POST'])
    def kadmos_revert_step():
        """
           Function to revert the last graph manipulation step by returning the _backup file from the tepm folder
           :return: the graph compressed as VISTOMS data
        """
        try:
            # get request form
            graphID = request.form['graphID']

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            tmpDir = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            backupGraphFileName = TEMP_FILE + '_' + graphID + '_backup.kdms'
            backupMpgFileName = TEMP_FILE + '_' + graphID + '_backup_mpg.kdms'

            graph = load(os.path.join(tmpDir, graphFileName), file_check_critical=False)
            backupGraph = load(os.path.join(tmpDir, backupGraphFileName), file_check_critical=False)
            if os.path.exists(os.path.join(tmpDir, mpgFileName)):
                mpg = load(os.path.join(tmpDir, mpgFileName), file_check_critical=False)
                os.remove(os.path.join(tmpDir, mpgFileName))
            else:
                mpg = None

            if os.path.exists(os.path.join(tmpDir, backupMpgFileName)):
                backupMpg = load(os.path.join(tmpDir, backupMpgFileName), file_check_critical=False)
                os.remove(os.path.join(tmpDir, backupMpgFileName))
            else:
                backupMpg = None

            # Switch graph and backup graph (What used to be the backup graph is now the new graph and vice versa)
            graph.save(os.path.join(upload_folder, backupGraphFileName), file_type="kdms", graph_check_critical=False,
                       mpg=mpg)
            backupGraph.save(os.path.join(upload_folder, graphFileName), file_type="kdms", graph_check_critical=False,
                             mpg=backupMpg)

            # Get function_oder of the backup graph
            function_order = None
            if backupGraph.graph_has_nested_attributes('problem_formulation', 'function_order'):
                function_order = backupGraph.graph['problem_formulation']['function_order']

            newVistomsData = backupGraph.vistoms_add_json(function_order=function_order,  mpg=backupMpg, graph_id=graphID)

            return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    def savePreviousGraph(graph_id, upload_folder):
        """
            Function saves the last graph, so you can revert a graph change within VISTOMS

            :param graph: Initial fundamental problem graph (FPG) to start working on the MDAO architecture definition
            :return: New VISTOMS json data with initial FPG
        """
        path = upload_folder
        # current graph and mpg name
        graphFileName = TEMP_FILE + '_' + graph_id + '.kdms'
        mpgFileName = TEMP_FILE + '_' + graph_id + '_mpg.kdms'

        # Save graph as backup file
        backupGraphFileName = TEMP_FILE + '_' + graph_id + '_backup.kdms'
        copyfile(os.path.join(path, graphFileName), os.path.join(path, backupGraphFileName))
        if os.path.exists(os.path.join(path, mpgFileName)):
            # If mpg exists, save it as well
            backupMpgFileName = TEMP_FILE + '_' + graph_id + '_mpg_backup.kdms'
            copyfile(os.path.join(path, mpgFileName), os.path.join(path, backupMpgFileName))

    def delete_backup_graphs(upload_folder):
        """
        Function deletes all graphs that end with a _backup
        """
        for file in os.listdir(upload_folder):
            if fnmatch.fnmatch(file, '*_backup*'):
                os.remove(os.path.join(upload_folder, file))
########################################################################################################################


    # Graph inspection functions
    ########################################################################################################################
    @app.route('/kadmos_find_all_nodes', methods=['POST'])
    def kadmos_find_all_nodes():
        """
            Function to get all nodes from certain categories and return them

            :param method: The method for sorting the nodes. Specified by the user from VISTOMS
            :return: New VISTOMS json data with updated design competences
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            category = str(request.form['category'])
            sub_category = str(request.form['sub_category'])
            attr_cond = ast.literal_eval(request.form['attr_cond'])
            attr_include = ast.literal_eval(request.form['attr_include'])
            attr_exclude = ast.literal_eval(request.form['attr_exclude'])
            xPath_include = str(request.form['xPath_include']).split(', ')
            xPath_exclude = str(request.form['xPath_exclude']).split(', ')

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = load(os.path.join(path, mpgFileName), file_check_critical=False)
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

            if attr_cond == []:
                attr_cond = None
            if attr_include == []:
                attr_include = None
            if attr_exclude == []:
                attr_exclude = None
            if xPath_include == [""]:
                xPath_include = None
            if xPath_exclude == [""]:
                xPath_exclude = None

            allNodes = graph.find_all_nodes(category=category, subcategory=sub_category, attr_cond=attr_cond,
                                            attr_include=attr_include, attr_exclude=attr_exclude,
                                            xpath_include=xPath_include, xpath_exclude=xPath_exclude)

            # allNodes_str = ', '.join(str(e) for e in allNodes)
            allNodes_str = json.dumps(allNodes)

            return allNodes_str

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_L1_check', methods=['POST'])
    def kadmos_L1_check():
        """
            Function to perform category a checks on the graph

            :return: Message, whether the check was successful or not
        """
        try:
            # Get request form
            graphID = request.form['graphID']

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = load(os.path.join(path, mpgFileName), file_check_critical=False)
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

            check_result = graph._check_category_a()

            if check_result[0] == True:
                return ("Check successful!")
            else:
                return "ERROR: Check was not successful. For further information, please consult the python log"

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_L2_check', methods=['POST'])
    def kadmos_L2_check():
        """
            Function to perform category b checks on the graph

            :return: Message, whether the check was successful or not
        """
        try:
            # Get request form
            graphID = request.form['graphID']

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = load(os.path.join(path, mpgFileName), file_check_critical=False)
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

            check_result = graph._check_category_b()

            if check_result[0] == True:
                return ("Check successful!")
            else:
                return "ERROR: Check was not successful. For further information, please consult the python log"

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_L3_check', methods=['POST'])
    def kadmos_L3_check():
        """
            Function to perform category c checks on the graph

            :return: Message, whether the check was successful or not
        """
        try:
            # Get request form
            graphID = request.form['graphID']

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = load(os.path.join(path, mpgFileName), file_check_critical=False)
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

            check_result = graph._check_category_c()

            if check_result[0] == True:
                return ("Check successful!")
            else:
                return "ERROR: Check was not successful. For further information, please consult the python log"

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    ########################################################################################################################


    # Upload custom kadmos script
    ########################################################################################################################
    @app.route('/kadmos_run_custom_script', methods=['POST'])
    def kadmos_run_custom_script():
        """
            Generic function to import and execute a custom kadmos script

            :param script_file: the custom kadmos script
            :param graph: the kadmos graph, on which the changes are performed
            :return: newVistomsData: Merged string of the vistoms data and the script string value
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            uploaded_files = request.files.getlist("file[]")

            script_file = []
            for aFile in uploaded_files:
                file_type = aFile.filename.rsplit('.', 1)[1].lower()
                if not file_type == "py":
                    return "ERROR: wrong file type \"" + file_type + "\""
                script_file = aFile

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID)

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = load(os.path.join(path, mpgFileName), file_check_critical=False)
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

            # save kadmos script in temp folder
            script_file.save(os.path.join(upload_folder, script_file.filename))
            kadmos_file_path = os.path.join(upload_folder, script_file.filename)

            # execute script and return graph data (graph, mpg)
            import imp
            script_module = imp.load_source('kadmos_custom_fun_{}', kadmos_file_path)
            graph, mpg = script_module.script(graph, mpg)

            # Get function order for VISTOMS in case of FPG
            function_order = None
            if mpg == None:
                # Get function_oder of the graph after the script has done the manipulations
                if graph.graph_has_nested_attributes('problem_formulation', 'function_order'):
                    function_order = graph.graph['problem_formulation']['function_order']

            # Add modified graph to VISTOMS
            newVistomsData = graph.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
            # Save the graph in temp/tmp.kdms
            graph.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                       graph_check_critical=False, mpg=mpg)
            return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    ########################################################################################################################


    # FPG manipulation functions
    ########################################################################################################################
    @app.route('/kadmos_start_defining_MDO_problem', methods=['POST'])
    def kadmos_start_defining_MDO_problem():
        """
            Function to start an MDO problem

            :param fpg_initial: Initial fundamental problem graph (FPG) to start working on the MDO problem definition
            :return: New VISTOMS json data with initial FPG
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            functionOrder = request.form['currentOrder'].split(',')
            newGraphID = request.form['newGraphID']
            newGraphName = request.form['newGraphName']

            newFileName = TEMP_FILE + '_' + newGraphID + '.kdms'

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ("ERROR: Graph is already an MDPG! FPG Cannot be initialized again!")
            else:
                mpg = None

                graph = load(os.path.join(path, graphFileName), file_check_critical=False)

                if isinstance(graph, FundamentalProblemGraph):
                    return ("ERROR: Graph is already an FPG and cannot be initialized again!")
                fpg_initial = graph.deepcopy_as(FundamentalProblemGraph)

                fpg_initial.graph['name'] = newGraphName
                fpg_initial.graph['description'] = 'Fundamental problem graph to solve the "' + graph.graph[
                    'name'] + '".'
                fpg_initial.graph['problem_formulation'] = dict()
                fpg_initial.graph['problem_formulation']['function_order'] = functionOrder
                fpg_initial.graph['problem_formulation']['mdao_architecture'] = "None"

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg_initial.vistoms_add_json(graph_id=newGraphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg_initial.save(os.path.join(upload_folder, newFileName), file_type="kdms", graph_check_critical=False,
                                 mpg=mpg)

                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.


    @app.route('/kadmos_add_DC_metadata', methods=['POST'])
    def kadmos_add_DC_metadata():
        """
            Function adds metadata to a dc in the graph
            :param graphID: ID of the current graph
            :return: VISTOMS json data with graph information
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')
            nodeName = request.form['nodeName']
            metadata_str = request.form['metadata_str']

            # read json data
            metadata_py = json.loads(metadata_str)

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID)

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return "ERROR: You cannot add metadata to a design competence in an MPG! Please go back to the RCG to do so."
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                graph.add_dc_general_info(nodeName,
                                          description=metadata_py['description'],
                                          status=metadata_py['status'],
                                          owner_uid=metadata_py['owner_uid'],
                                          creator_uid=metadata_py['creator_uid'],
                                          operator_uid=metadata_py['operator_uid'])

                ### Functions do not exist yet ###
                ###################################
                # graph.add_dc_licensing(nodeName,
                #                         license_type=metadata_py['license_type'],
                #                         license_specification=metadata_py['license_specification'],
                #                         license_info=metadata_py['license_info'])
                # graph.add_dc_sources(nodeName,
                #                       repository_link=metadata_py['repository_link'],
                #                       download_link=metadata_py['download_link'],
                #                       references=[metadata_py['references']])
                # graph.add_dc_execution_details(nodeName,
                #                                 operating_system=metadata_py['operating_system'],
                #                                 integration_platform=metadata_py['integration_platform'],
                #                                 command=metadata_py['command'],
                #                                 description=metadata_py['description_cmd'],
                #                                 software_requirements=[metadata_py['software_requirements']],
                #                                 hardware_requirements=metadata_py['hardware_requirements'],)
                ###################################

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = graph.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Use function order for VISTOMS if it is available in the graph information
                if graph.graph_has_nested_attributes('problem_formulation', 'function_order') and mpg == None:
                    graph.graph['problem_formulation']['function_order'] = function_order
                # Save the graph in temp/tmp.kdms
                graph.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                           graph_check_critical=False, mpg=mpg)

                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.


    @app.route('/kadmos_add_mathematical_function', methods=['POST'])
    def kadmos_add_mathematical_function():
        """
            Function adds a mathematical function to the graph
            :param graphID: ID of the current graph
            :return: VISTOMS json data with graph information
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            function_order = []
            if request.form['currentOrder'] != '':
                function_order = request.form['currentOrder'].split(',')
            form_data_str = request.form['form_data']

            # convert stringified data into python objects/arrays/.. with json.loads function
            form_data_py = json.loads(form_data_str)

            # Get information from form_data_py
            function_node = form_data_py['function_node']
            input_nodes_xPath = form_data_py['input_nodes_xPath'].split(',')
            input_nodes_name = form_data_py['input_nodes_name'].split(',')
            output_node_xPath = form_data_py['output_node_xPath']
            equation = form_data_py['equation']
            language = form_data_py['language']

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes to the graph
            savePreviousGraph(graphID)

            # Load the current graph from the temporary folder
            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return "ERROR: You cannot add a design competence to an MPG! Please go back to the RCG to do so."
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                # Get input_nodes and output_nodes from request form data
                input_nodes = []
                for idx, xPath in enumerate(input_nodes_xPath):
                    input_node = [xPath, input_nodes_name[idx]]
                    input_nodes.append(input_node)
                output_nodes = [[output_node_xPath, equation, language]]

                # Add the new mathematical function to the graph as a new competence block
                graph.add_mathematical_function(input_nodes=input_nodes, function_node=function_node,
                                                output_nodes=output_nodes)

                # Add the new mathematical function to the function list (function_order)
                function_order.append(function_node)

                # The graph with the added mathematical function is now saved as json data for vistoms
                newVistomsData = graph.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Use function order for VISTOMS if it is available in the graph information
                if graph.graph_has_nested_attributes('problem_formulation', 'function_order') and mpg == None:
                    graph.graph['problem_formulation']['function_order'] = function_order
                # Save the graph in temp/tmp.kdms
                graph.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                           graph_check_critical=False, mpg=mpg)

                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.


    @app.route('/kadmos_add_design_competence', methods=['POST'])
    def kadmos_add_design_competence():
        """
            Function adds a dc to the graph
            :param graphID: ID of the current graph
            :return: VISTOMS json data with graph information
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            input_file = request.form['input']
            output_file = request.form['output']
            cmdows_file = request.form['cmdows']

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID)

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ("ERROR: You cannot add a design competence to an MPG! Please go back to the RCG to do so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                # Here the dc cmdows file and database is created
                check_list = ['consistent_root', 'invalid_leaf_elements']
                graph_dc = load(check_list=check_list)

                # Here the two graphs are merged
                new_graph = nx.compose(graph, graph_dc)

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = new_graph.vistoms_add_json(graph_id=graphID, mpg=mpg)

                # Save the graph in temp/tmp.kdms
                new_graph.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                               graph_check_critical=False, mpg=mpg)

                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.


    @app.route('/kadmos_change_node_pos', methods=['POST'])
    def kadmos_change_node_pos():
        """
            Function to change the position of a node (competence) within the graph

            :param newPos: Initial fundamental problem graph (FPG) to start working on the MDO problem definition
            :return: New VISTOMS json data with initial FPG
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            nodeName = str(request.form['nodeName'])
            function_order = request.form['currentOrder'].split(',')
            newPos = int(request.form['newPos'])

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return (
                    "ERROR: You cannot change a competence's position on an existing MPG! Please go back to the FPG or "
                    "RCG to do so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                # Change position of a node in th XDSM

                # Get tool list and put the coordinator in the top left corner
                function_order.remove(nodeName)
                function_order.insert(newPos, nodeName)
                if isinstance(graph, FundamentalProblemGraph):
                    graph.graph['problem_formulation']['function_order'] = function_order
                    if 'problem_role' in graph.nodes[function_order[0]]:
                        graph.add_function_problem_roles()

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = graph.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                graph.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                           graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_delete_node', methods=['POST'])
    def kadmos_delete_node():
        """
            Function deletes a node from the graph and returns the updated graph data to VISTOMS
            :param nodeName: name of the node to be deleted
            :return: VISTOMS json data with graph information
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            nodeName = str(request.form['nodeName'])
            function_order = request.form['currentOrder'].split(',')

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return (
                    "ERROR: You cannot remove a competence from an existing MPG! Please go back to the FPG or RCG to "
                    "do so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                # remove the node from the graph
                graph.remove_function_nodes(nodeName)
                # update function order
                function_order.remove(nodeName)

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = graph.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                graph.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                           graph_check_critical=False, mpg=mpg)

                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_delete_edge', methods=['POST'])
    def kadmos_delete_edge():
        """
            Function deletes an edge from the graph and returns the updated graph data to VISTOMS
            :param nodeName: name of the node that is the input provider of the edge
            :param edgeName: name of the edge to be deleted
            :return: VISTOMS json data with graph information
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            nodeName = str(request.form['nodeName'])
            edgeName = str(request.form['edgeName'])
            function_order = request.form['currentOrder'].split(',')

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = load(os.path.join(path, mpgFileName), file_check_critical=False)
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

            # remove the edge
            graph.remove_edge(nodeName, edgeName)
            # Add the graph with the updated function order to VISTOMS
            newVistomsData = graph.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
            # Save the graph in temp/tmp.kdms
            graph.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                       graph_check_critical=False, mpg=mpg)

            return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_exclude_DCs', methods=['POST'])
    def kadmos_exclude_DCs():
        """
            Function to exclude design competences as requested by the user from VISTOMS

            :param nodeList: List of competences that shall be excluded
            :return: New VISTOMS json data with excluded design competences deleted
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            nodeList = request.form['nodeList'].split(',')
            function_order = request.form['currentOrder'].split(',')

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return (
                    "ERROR: You cannot remove a competence from an existing MPG! Please go back to the FPG or RCG to "
                    "do so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                fpg = FundamentalProblemGraph(graph)

                # Remove a node from the graph
                for nodeName in nodeList:
                    fpg.remove_function_nodes(nodeName)
                    function_order.remove(nodeName)
                # Assign new function order to problem formulation
                fpg.graph['problem_formulation']['function_order'] = function_order

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_merge_seq_DCs', methods=['POST'])
    def kadmos_merge_seq_DCs():
        """
            Function to merge design competences that run sequentially as requested by the user from VISTOMS

            :param nodeList: List of competences that shall be merged
            :return: New VISTOMS json data with merged design competences
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')
            nodeList = request.form['nodeList'].split(',')

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return (
                    "ERROR: You cannot merge comeptences on an existing MPG! Please go back to the FPG or RCG to do "
                    "so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                new_node = '-'.join(nodeList) + '--seq'

                if isinstance(graph, FundamentalProblemGraph):
                    fpg = graph
                else:
                    fpg = FundamentalProblemGraph(graph)

                fpg = fpg.merge_sequential_functions(nodeList, new_label=new_node)
                # adjust function order
                function_order = [new_node if func == nodeList[0] else func for func in function_order]
                for func in nodeList[1:]:
                    function_order.remove(func)
                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_merge_parallel_DCs', methods=['POST'])
    def kadmos_merge_parallel_DCs():
        """
            Function to merge design competences that run in parallel as requested by the user from VISTOMS

            :param nodeList: List of competences that shall be merged
            :return: New VISTOMS json data with merged design competences
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')
            nodeList = request.form['nodeList'].split(',')

            # Load upload_folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return (
                    "ERROR: You cannot merge comeptences on an existing MPG! Please go back to the FPG or RCG to do "
                    "so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                new_node = '-'.join(nodeList) + '--par'

                if isinstance(graph, FundamentalProblemGraph):
                    fpg = graph
                else:
                    fpg = FundamentalProblemGraph(graph)

                fpg = fpg.merge_parallel_functions(nodeList, new_label=new_node)
                # adjust function order
                function_order = [new_node if func == nodeList[0] else func for func in function_order]
                for func in nodeList[1:]:
                    function_order.remove(func)

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_merge_func_mod_DCs', methods=['POST'])
    def kadmos_merge_func_mod_DCs():
        """
            Function to merge design competences that run in different modes as requested by the user from VISTOMS

            :param nodeList: List of competences that shall be merged
            :return: New VISTOMS json data with merged design competences
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')
            nodeList = request.form['nodeList'].split(',')

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return (
                    "ERROR: You cannot merge comeptences on an existing MPG! Please go back to the FPG or RCG to do "
                    "so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                if isinstance(graph, FundamentalProblemGraph):
                    fpg = graph
                else:
                    fpg = FundamentalProblemGraph(graph)

                base_function = fpg.node[nodeList[0]]['name']
                modes = [str(string[string.find('[') + 1:string.find(']')]) for string in nodeList]
                suffices = [str(string[string.find('_'):string.find('[')]) for string in nodeList]
                new_node = base_function + '-merged[' + str(len(nodeList)) + 'modes]'

                fpg = fpg.merge_function_modes(base_function, modes, new_label=new_node, version='1.0', instance=1,
                                               suffices=suffices)
                # adjust function order
                function_order = [new_node if func == nodeList[0] else func for func in function_order]
                for func in nodeList[1:]:
                    function_order.remove(func)

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_remove_collision', methods=['POST'])
    def kadmos_remove_collision():
        """
            Function to remove collisions coming from specific design competences as requested by the user from VISTOMS

            :param nodeList: List of competences for which collisions should be removed
            :return: New VISTOMS json data with updated design competences
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            nodeList = request.form['nodeList'].split(',')
            function_order = request.form['currentorder'].split(',')

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return (
                    "ERROR: You cannot merge comeptences on an existing MPG! Please go back to the FPG or RCG to do "
                    "so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                if isinstance(graph, FundamentalProblemGraph):
                    fpg = graph
                else:
                    fpg = FundamentalProblemGraph(graph)

                for collision_source in nodeList:
                    fpg.disconnect_problematic_variables_from(collision_source)

                    fpg.graph['problem_formulation']['function_order'] = function_order

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_get_possible_function_order', methods=['POST'])
    def kadmos_get_possible_function_order():
        """
            Function to get a possible function order

            :param method: The method for sorting the nodes. Specified by the user from VISTOMS
            :return: New VISTOMS json data with updated design competences
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            method = request.form['sortingMethod']

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return (
                    "ERROR: You cannot merge comeptences on an existing MPG! Please go back to the FPG or RCG to do "
                    "so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                if isinstance(graph, FundamentalProblemGraph):
                    fpg = graph
                else:
                    fpg = FundamentalProblemGraph(graph)

                # Getting the possible function order with the method specified by the user
                function_order = fpg.get_possible_function_order(method)
                fpg.assert_or_add_nested_attribute(['problem_formulation', 'mdao_architecture'], 'undefined')
                fpg.graph['problem_formulation']['function_order'] = function_order
                if 'problem_role' in fpg.nodes[function_order[0]]:
                    fpg.add_function_problem_roles()

                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)

                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_make_all_variables_valid', methods=['POST'])
    def kadmos_make_all_variables_valid():
        """
            Function to make all variables from the graph valid --> Eliminates colissions

            :return: New VISTOMS json data with updated design competences
        """
        try:
            # get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ("ERROR: You cannot do that on an existing MPG! Please go back to the FPG or RCG to do so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                if isinstance(graph, FundamentalProblemGraph):
                    fpg = graph
                else:
                    fpg = FundamentalProblemGraph(graph)

                fpg.graph['problem_formulation']['function_order'] = function_order

                # Function to check the graph for collisions and holes. Collisions are solved based on the function order
                # and holes will simply be removed.
                fpg.make_all_variables_valid()

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_add_function_problem_roles', methods=['POST'])
    def kadmos_add_function_problem_roles():
        """
            Function to Add the problem function roles to the graph

            :return: New VISTOMS json data with updated design competences
        """
        try:
            # get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ("ERROR: You cannot do that on an existing MPG! Please go back to the FPG or RCG to do so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                if isinstance(graph, FundamentalProblemGraph):
                    fpg = graph
                else:
                    fpg = FundamentalProblemGraph(graph)

                fpg.graph['problem_formulation']['function_order'] = function_order

                # Add the function problem roles (pre-coupling, coupled, post-coupling)
                fpg.add_function_problem_roles()

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_mark_variable', methods=['POST'])
    def kadmos_mark_variable():
        """
            Function to mark a variable as "special variable" (constraint, objective, design variable, quantity of interest)
            :param xPath: xPath of the variable in the XML schema
            :param variableType: type of the variable it shall be marked as (constraint, objective, design variable,
                quantity of interest)
            :return: VISTOMS json data with graph information
        """
        try:
            # get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')
            variableType = request.form['variableType']
            xPath = request.form['xPath']
            operator = request.form['operator']
            upperBound = float(request.form['upperBound'])
            lowerBound = float(request.form['lowerBound'])
            nominalValue = float(request.form['nominalValue'])

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ('ERROR: This function can only be performed on an FPG!')
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

            if isinstance(graph, FundamentalProblemGraph):
                fpg = graph
            else:
                fpg = FundamentalProblemGraph(graph)

            if (variableType == 'designVariable'):
                fpg.mark_as_design_variable(xPath, nominal_value=nominalValue, upper_bound=upperBound,
                                            lower_bound=lowerBound)
            elif (variableType == 'objective'):
                fpg.mark_as_objective(xPath)
            elif (variableType == 'constraint'):
                fpg.mark_as_constraint(xPath, reference_value=nominalValue, operator=operator)
            elif (variableType == 'quantityOfInterest'):
                fpg.mark_as_qois([xPath])
            else:
                return ("ERROR: Something went wrong in KADMOS!")

            # Add the graph with the updated function order to VISTOMS
            newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
            # Save the graph in temp/tmp.kdms
            fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                     graph_check_critical=False, mpg=mpg)

            return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_unmark_variable', methods=['POST'])
    def kadmos_unmark_variable():
        """
            Function to unmark a previously marked variable
            :param xPath: xPath of the variable in the XML schema
            :return: VISTOMS json data with graph information
        """
        try:
            # get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')
            xPath = request.form['xPath']

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ('ERROR: This function can only be performed on an FPG!')
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

            if isinstance(graph, FundamentalProblemGraph):
                fpg = graph
            else:
                fpg = FundamentalProblemGraph(graph)

            fpg.unmark_variable(xPath)

            # Add the graph with the updated function order to VISTOMS
            newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
            # Save the graph in temp/tmp.kdms
            fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'), file_type='kdms',
                     graph_check_critical=False, mpg=mpg)

            return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_remove_unused_outputs', methods=['POST'])
    def kadmos_remove_unused_outputs():
        """
            Function to remove all unused variables that are output to the coordinator

            :return: New VISTOMS json data with updated design competences
        """
        try:
            # get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')
            cleanUp_str = request.form['cleanUp']
            if cleanUp_str == 'True':
                cleanUp = True
            else:
                cleanUp = False

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ("ERROR: You cannot do that on an existing MPG! Please go back to the FPG or RCG to do so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                if isinstance(graph, FundamentalProblemGraph):
                    fpg = graph
                else:
                    fpg = FundamentalProblemGraph(graph)

                fpg.graph['problem_formulation']['function_order'] = function_order

                # Cleaning of the graph needs to be done in a while loop, to entirely remove all unused elements
                another_run = True
                while another_run:
                    another_run = False
                    # Delete unused variables
                    output_nodes = fpg.find_all_nodes(subcategory='all outputs')
                    for output_node in output_nodes:
                        if 'problem_role' not in fpg.node[output_node]:
                            fpg.remove_node(output_node)
                            another_run = True
                    # Delete unnecessary functions automatically if the user wants to
                    if cleanUp:
                        function_nodes = fpg.find_all_nodes(category='function')
                        for function_node in function_nodes:
                            if not fpg.out_edges(function_node):
                                fpg.remove_function_nodes(function_node)
                                function_order.remove(function_node)
                                another_run = True

                # Add the function problem roles (pre-coupling, coupled, post-coupling)
                fpg.add_function_problem_roles()

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = fpg.vistoms_add_json(function_order=function_order, graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                fpg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    ########################################################################################################################

    # MDPG manipulation functions
    ########################################################################################################################
    @app.route('/kadmos_start_defining_MDAO_architecture', methods=['POST'])
    def kadmos_start_defining_MDAO_architecture():
        """
            Function to start an MDO problem definition

            :param graph: Initial fundamental problem graph (FPG) to start working on the MDAO architecture definition
            :return: New VISTOMS json data with initial FPG
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            functionOrder = request.form['currentOrder'].split(',')
            newGraphID = request.form['newGraphID']
            newGraphName = request.form['newGraphName']

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            newFileName = TEMP_FILE + '_' + newGraphID + '.kdms'

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ("ERROR: Graph is already an MDPG! FPG Cannot be initialized again!")
            else:
                mpg = None

                graph = load(os.path.join(path, graphFileName), file_check_critical=False)

                if not isinstance(graph, FundamentalProblemGraph):
                    return ("ERROR: Graph is not an FPG yet. Please perform the FPG Manipulation steps first!")

                # check if fpg is well defined
                check_result = graph._check_category_a()
                if check_result[0] != True:
                    return (
                        "ERROR: The FPG is not well defined yet. Please perform FPG manipulation steps first and check "
                        "the graph again!")

                mdg = deepcopy(graph)
                mdg.graph['name'] = newGraphName
                mdg.graph['description'] = 'MDAO data and process graph to solve the "' + graph.graph['name'] + '".'
                mdg.graph['problem_formulation'] = dict()
                mdg.graph['problem_formulation']['function_order'] = functionOrder
                mdg.graph['problem_formulation']['mdao_architecture'] = "None"

                # Add the graph with the updated function order to VISTOMS
                newVistomsData = mdg.vistoms_add_json(function_order=functionOrder, graph_id=newGraphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                mdg.save(os.path.join(upload_folder, newFileName), file_type="kdms", graph_check_critical=False,
                         mpg=mpg)

                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    @app.route('/kadmos_impose_MDAO_architecture', methods=['POST'])
    def kadmos_impose_MDAO_architecture():
        """
            Function to wrap an MDAO architecture around the MDAO problem

            :param allowUnconvergedCouplings: Bool variable whether unconverged couplings are allowed or not
            :return: New VISTOMS json data with updated MDAO data and process graphs
        """
        try:
            # Get request form
            graphID = request.form['graphID']
            function_order = request.form['currentOrder'].split(',')
            mdao_architecture = request.form['mdao_architecture']
            doe_method = request.form['doe_method']
            coupling_decomposition = request.form['coupling_decomposition']
            allow_unconverged_couplings_str = request.form['allow_unconverged_couplings']
            if allow_unconverged_couplings_str == 'True':
                allow_unconverged_couplings = True
            else:
                allow_unconverged_couplings = False

            # Load upload folder based on session
            sessionID = request.form['sessionID']
            upload_folder = UPLOAD_FOLDERS[sessionID]

            # Save previous graph as backup before making the changes
            savePreviousGraph(graphID, upload_folder)

            path = upload_folder
            graphFileName = TEMP_FILE + '_' + graphID + '.kdms'
            mpgFileName = TEMP_FILE + '_' + graphID + '_mpg.kdms'
            if os.path.exists(os.path.join(path, mpgFileName)):
                return ("ERROR: You cannot perform this on an existing MPG! Please go back to the FPG to do so.")
            else:
                graph = load(os.path.join(path, graphFileName), file_check_critical=False)
                mpg = None

                mdao_definition = mdao_architecture
                if coupling_decomposition == 'Gauss-Seidel':
                    mdao_definition += '-GS'
                elif coupling_decomposition == 'Jacobi':
                    mdao_definition += '-J'
                elif coupling_decomposition == '-':
                    coupling_decomposition = None

                if not isinstance(graph, FundamentalProblemGraph):
                    return "ERROR: Your graph is not an FPG yet. Please perform FPG manipulation steps before imposing an" \
                           " MDAO architecture!"

                fpg = graph

                mdao_definition = mdao_architecture
                if coupling_decomposition == 'Gauss-Seidel':
                    mdao_definition += '-GS'
                elif coupling_decomposition == 'Jacobi':
                    mdao_definition += '-J'
                elif coupling_decomposition == '-':
                    coupling_decomposition = None

                # Define settings of the problem formulation
                fpg.graph['problem_formulation'] = dict()
                fpg.graph['problem_formulation']['function_order'] = function_order
                fpg.graph['problem_formulation']['mdao_architecture'] = mdao_architecture
                fpg.graph['problem_formulation']['convergence_type'] = coupling_decomposition
                fpg.graph['problem_formulation']['allow_unconverged_couplings'] = allow_unconverged_couplings

                if mdao_architecture in ['converged-DOE', 'unconverged-DOE']:
                    if doe_method not in fpg.OPTIONS_DOE_METHODS:
                        return "ERROR: Invalid DOE method selected, please select a DOE method from the dropdown list"

                    fpg.graph['problem_formulation']['doe_settings'] = {'doe_method': doe_method}
                    if fpg.graph['problem_formulation']['doe_settings']['doe_method'] in ['Latin hypercube design',
                                                                                          'Monte Carlo design']:
                        fpg.graph['problem_formulation']['doe_settings']['doe_seed'] = 6
                        fpg.graph['problem_formulation']['doe_settings']['doe_runs'] = 5
                    elif fpg.graph['problem_formulation']['doe_settings']['doe_method'] in ['Full factorial design']:
                        fpg.graph['problem_formulation']['doe_settings']['doe_runs'] = 5

                fpg.add_function_problem_roles()

                mdg, mpg = fpg.impose_mdao_architecture()

                mpg.graph['name'] = 'XDSM - {}'.format(mdao_definition)
                mpg.graph['description'] = 'Solution strategy to solve the super-sonic business jet test case ' \
                                           'optimization problem using the strategy: {}.'.format(mdao_definition)
                # Add the graph with the updated function order to VISTOMS
                newVistomsData = mdg.vistoms_add_json(graph_id=graphID, mpg=mpg)
                # Save the graph in temp/tmp.kdms
                mdg.save(os.path.join(upload_folder, TEMP_FILE + '_' + graphID + '.kdms'),
                         file_type='kdms', graph_check_critical=False, mpg=mpg)
                return newVistomsData

        except Exception as e:
            return "ERROR: " + e.message
            # Logs the error appropriately.

    ########################################################################################################################

    # Return the interface
    return app
