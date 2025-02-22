:orphan:

******************************
4. Putting everything together
******************************

In the code below, we put together the **TrainWork**, the **MLServer** and the **Locust** components in an ``app.py`` file.

.. literalinclude:: ./app.py


***********
Run the App
***********

To run the app, simply open a terminal and execute this command:

.. code-block:: bash

    lightning run app docs/source-app/examples/model_deploy_app/app.py

Here is a gif of the UI.

.. figure::  https://pl-flash-data.s3.amazonaws.com/assets_lightning/ml_server_2.gif

.. raw:: html

    <br />

Congrats, you have finished the **Build a Model Server** example !

----

******************
Find more examples
******************

.. raw:: html

    <div class="display-card-container">
        <div class="row">

.. Add callout items below this line

.. displayitem::
   :header: Build a DAG
   :description: Create a dag pipeline
   :col_css: col-md-4
   :button_link: ../dag/dag.html
   :height: 150
   :tag: Intermediate

.. displayitem::
   :header: Build a File Server
   :description: Train multiple models with different parameters
   :col_css: col-md-4
   :button_link: ../file_server/file_server.html
   :height: 150
   :tag: Intermediate

.. displayitem::
   :header: Build a Github Repo Script Runner
   :description: Run code from the internet in the cloud
   :col_css: col-md-4
   :button_link: ../github_repo_runner/github_repo_runner.html
   :height: 150
   :tag: Intermediate

.. displayitem::
   :header: Build a HPO Sweeper
   :description: Train multiple models with different parameters
   :col_css: col-md-4
   :button_link: ../hpo/hpo.html
   :height: 150
   :tag: Intermediate

.. raw:: html

        </div>
    </div>
