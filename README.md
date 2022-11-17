# MLOpsCapstoneProject

Project created with MLOps-Template cookiecutter. For more info: https://mlopsstudygroup.github.io/mlops-guide/


## 📋 Requirements

* DVC
* Python3 and pip

Create a virtual environment
```
python3 -m venv mlopsenv
```

Activate the virtual env
```
source mlopsenv/bin/activate  
```

To install dependencies 
```bash
pip install -r requirements.txt
```

## 🏃🏻 Running Project



### ⚗️ Using DVC
Initialize dvc
```
dvc init
```

To set the remote storage service on Firebase
```
dvc remote add -d storage gs://mlops-85438.appspot.com
```

To configure credentials ask the team for the `mlops-storage-key.json` file
```
export GOOGLE_APPLICATION_CREDENTIALS=mlops-storage-key.json
```

In this point we are ready to go! 🚀🚀

#### How to use `dvc`
Once we have seted up dvc, we can `add`, `pull` or `push` the data we wish.

Similar to `git add file_path`, `dvc add file_path` adds the files to the dvc versioning 
```
dvc add file_path
```

Uploads data from the DVC repository(analog to ```git push```)
```
dvc push
```

Download data from the DVC repository(analog to ```git pull```)
```
dvc pull
```

#### *Versioning our data*
To setup a data version
```
git tag -a version_name -m "This is a comment to reference this data version" 
```

To push the `data.dvc` versioned file to git
```
git push origin --tags
```

#### Use case
Lets supose we have some new data we want to add dvc versioning.
1. Add the new data
```
dvc add data
```

2. Push The changes to our storage bucker
```
dvc push data
```

3. Generate new tag
```
git tag -a new_version_name -m "New version of the data"
git add .
git commit -m "New data version"
git push
git push origin --tags
```

In this point we have a new data version, each of this versions have different 'data.dvc' for each version


To change from data version `versionA` to `versionB`
```
git checkout tags/versionB # this changes the `data.dvc` file to the versionB branch
dvc pull # this brings the data from  versionB tag
```


### Bring the initial dvc data to your local environment
