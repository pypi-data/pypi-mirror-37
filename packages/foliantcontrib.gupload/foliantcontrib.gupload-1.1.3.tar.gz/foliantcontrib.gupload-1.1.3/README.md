# Documents to Google Drive uploader for Foliant

Gupload is the Foliant CLI extension, it's used to upload created documents to Google Drive.

Gupload adds `gupload` command to Foliant.


## Installation

```shell
$ pip install foliantcontrib.gupload
```


## Config

To config the CLI extension, add `gupload` section in the project config. As `gupload` needs document to upload, appropriate backend settings also have to be here.

CLI extension has a number of options (all fields are required but can have no values):

```yaml
gupload:
    gdrive_folder_name: Foliant upload
    gdrive_folder_id:
    gdoc_title:
    gdoc_id:
    convert_file:
    com_line_auth: false
```

`gdrive_folder_name`
:   Folder with this name will be created on Google Drive to upload file.

`gdrive_folder_id`
:   This field is necessary to upload files to previously created folder.

`gdoc_title`
:   Uploaded file will have this title. If empty, real filename will be used.

`gdoc_id`
:   This field is necessary to rewrite previously uploaded file and keep the link to it.

`convert_file`
:   Convert uploaded files to google docs format or not.

`com_line_auth`
:   In some cases it's impossible to authenticate automatically (for example, with Docker), so you can set *True* and use command line authentication procedure.


## Usage

At first you have to get Google Drive authentication file.

1. Go to [APIs Console](https://console.developers.google.com/cloud-resource-manager) and make your own project.
2. Go to [library](https://console.developers.google.com/apis/library), search for ‘Google Drive API’, select the entry, and click ‘Enable’.
3. Select ‘Credentials’ from the left menu, click ‘Create Credentials’, select ‘OAuth client ID’.
4. Now, the product name and consent screen need to be set -> click ‘Configure consent screen’ and follow the instructions. Once finished:
    - Select ‘Application type’ to be *Other types*.
    - Enter an appropriate name.
    - Input http://localhost:8080 for ‘Authorized JavaScript origins’.
    - Input http://localhost:8080/ for ‘Authorized redirect URIs’.
    - Click ‘Save’.
5. Click ‘Download JSON’ on the right side of Client ID to download client_secret_<really long ID>.json. The downloaded file has all authentication information of your application.
6. Rename the file to “client_secrets.json” and place it in your working directory near foliant.yml.

Now add the CLI extension to the project config with all settings strings. At this moment you have no data to set *Google Drive folder ID* and *google doc ID* so keep it empty.

Run Foliant with `gupload` command:

```shell
$ foliant gupload docx
✔ Parsing config
✔ Applying preprocessor flatten
✔ Making docx with Pandoc
─────────────────────
Result: filename.docx
─────────────────────
✔ Parsing config
Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?...

Authentication successful.
✔ Uploading 'filename.docx' to Google Drive
─────────────────────
Result:
Doc link: https://docs.google.com/document/d/1GPvNSMJ4ZutZJwhUYM1xxCKWMU5Sg/edit?usp=drivesdk
Google drive folder ID: 1AaiWMNIYlq9639P30R3T9
Google document ID: 1GPvNSMJ4Z19YM1xCKWMU5Sg
```

Authentication form will be opened. Choose account to log in.

With command line authentication procedure differs little bit:

```
$ docker-compose run --rm foliant gupload docx
✔ Parsing config
✔ Applying preprocessor flatten
✔ Making docx with Pandoc
─────────────────────
Result: filename.docx
─────────────────────
✔ Parsing config
Go to the following link in your browser:

    https://accounts.google.com/o/oauth2/auth?...

Enter verification code: 4/XgBllTXpxv8kKjsiTxLc
Authentication successful.
✔ Uploading 'filename.docx' to Google Drive
─────────────────────
Result:
Doc link: https://docs.google.com/document/d/1GPvNSMJ4ZutZJwhUYM1xxCKWMU5Sg/edit?usp=drivesdk
Google drive folder ID: 1AaiWMNIYlq9639P30R3T9
Google document ID: 1GPvNSMJ4Z19YM1xCKWMU5Sg
```

Copy link from terminal to your browser, choose account to log in and copy generated code back to the terminal.

After that the document will be uploaded to Google Drive and opened in new browser tab.

Now you can use *Google Drive folder ID* to upload files to the same folder and *google doc ID* to rewrite document (also you can IDs in folder and file links).

### Notes

If you set up *google doc ID* without *Google Drive folder ID* file will be moved to the new folder with the same link.
