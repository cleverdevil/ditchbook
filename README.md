Ditchbook: Facebook to Micropub Toolkit
=======================================

Ditchbook is a toolkit for taking a high-fidelity Facebook JSON export, and
migrating selected content to your [Micropub](https://indieweb.org/micropub)
compatible website, including [Micro.blog](https://micro.blog) websites. Its a
great way to own your own data, and free yourself from Facebook.

Usage
-----

### Installation

First, you'll need to clone or download this project. Ditchbook requires Python
3.6 or greater to run. I recommend installing inside of a `virtualenv`:

```sh
$ git clone git@github.com:cleverdevil/ditchbook.git
$ cd ditchbook
$ virtualenv -p python3.6 venv
$ . venv/bin/activate
$ python setup.py develop
```

### Create a Facebook JSON Export

Once you've got a working installation, you'll need to create a Facebook export
[here](https://www.facebook.com/settings?tab=your_facebook_information). Select
`JSON` for the type of export and use high resolution photos. This can take a
few hours. Once you're done, download the ZIP file, and uncompress it into a
directory. Let's assume you've placed it in a directory called "export"
contained within your `ditchbook` directory.

### Ingest and Convert Facebook Data

Next, you'll want to run the `ingest` script, which will try and read in data
from your Facebook data, and then output it as standard
[microformats2](http://indieweb.org/microformats2) JSON data.

```sh
$ bin/ingest export
```

If all went well, you'll have a directory named `mf2` containing your converted
data. Huzzah!

### Configure Micropub

Next, copy `conf.py.sample` to `conf.py` and make the appropriate edits. You'll
need to provide your micropub endpoint, micropub media endpoint, micropub token,
and the destination.

In addition, you can configure a mapping of names to hyperlinks for when you've
got "mentions" of people in your content.

### Publish: Albums

Now, its time to publish your photo albums.

```sh
$ bin/publish-albums
```

Script will loop through the albums contained in your export, give you some
basic information about each one, and give you the choice of migrating an album
to your website, or not.

I'd recommend against uploading albums with many hundreds (or thousands) of
photos. Facebook creates an album called "Mobile Uploads" that tends to contain
every single photo ever uploaded with your iOS or Android device, and you're
better off not migrating that album. The photos themselves will be migrated as
"posts" in a future step, if you choose.

### Publish: Posts

Finally, you can publish other "posts" from Facebook, which includes notes,
status updates, and photos. Because the content isn't particularly well-suited
for migration, ditchbook will ignore many types of content, and focuses on the
types of data you'd like on your website. That means link sharing, events, and
other related data won't be migrated.

At this time, ditchbook doesn't support migrating videos. Maybe I'll get around
to it in the future. We'll see.

```sh
$ bin/publish-posts
```

This script will run in a similar fashion to the `publish-albums` script, but
will automatically publish posts that have at least one photo. Everything else
will ask you for confirmation.

Future
------

Ideally, I'd like to make this process easier and more seamless for end users.
Feel free to use the code to do that! I have no intention of using this code for
any commercial purpose, and instead and primarily motivated to help people free
themselves from Facebook, and control their own information.

Enjoy!

License
-------
This code is licensed under the MIT license.

Copyright 2018, Jonathan LaCour

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
