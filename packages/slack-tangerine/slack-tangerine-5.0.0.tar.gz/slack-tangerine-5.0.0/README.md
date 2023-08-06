<p align="center">
  <img src="https://raw.githubusercontent.com/nficano/tangerine/master/artwork/tangerine@2x.png" alt="Tangerine logo" width="307" height="77">
  <div align="center">
    <a href="https://travis-ci.org/nficano/tangerine"><img src="https://travis-ci.org/nficano/tangerine.svg?branch=master" /></a>
    <a href="https://pypi.org/project/pytangerine/"><img src="https://img.shields.io/pypi/v/pytangerine.svg#cachebust" alt="pypi"></a>
    <a href="https://pypi.python.org/pypi/pytangerine/"><img src="https://img.shields.io/pypi/pyversions/pytangerine.svg" /></a>
  </div>
</p>

A Flask inspired, decorator based API wrapper for Python-Slack.

## About

Tangerine is a lightweight Slackbot framework that abstracts away all the boilerplate code required to write bots, allowing you to focus on the problem at hand.

## Installation

1. To install tangerine, simply use pipenv (or pip, of course):

```bash
$ pipenv install slack-tangerine
```

2. Create a new file with the following contents:

```python
# mybot.py
from tangerine import Tangerine
tangerine = Tangerine("xoxb-1234567890-replace-this-with-token-from-slack")


@tangerine.listen_for('morning')
def morning(user, message):
    return "mornin' @{user.username}"

if __name__ == '__main__':
   tangerine.run()
 ```

3. Now try running it, run the following command then say "morning" in Slack.

```bash
python mybot.py
```

## Usage
To start your project, you'll first need to import tangerine by adding from tangerine import Tangerine to the top of your file.

Next you'll need to create an instance of Tangerine and configure your Slack token. This can be done using a yaml config file or passing it explicitly to the initialization.

```python
# Option 1: YAML config:
import os
from tangerine import Tangerine

path = os.path.dirname(os.path.abspath(__file__))
path_to_yaml = os.path.join(path, 'config.yaml')
tangerine = Tangerine.config_from_yaml(path_to_yaml)

# Option 2: Hardcoded slack token
from tangerine import Tangerine
tangerine = Tangerine("xoxb-1234567890-replace-this-with-token-from-slack")
```

Now its time to write your response functions, these functions get wrapped with the listen_for decorator, which registers a pattern to watch the slack conversation for and which python method should handle it once its said.

In the following example, the method is setup to listen for the word "cookies". Notice that the decorator passes two arguments to the function, first the user object which contains information about the user who triggered the event (in this case the Slack user who said the word cookies) and message, which is a string of the complete message.

```python
@tangerine.listen_for('cookies')
def cookies(user, message):
    # do something when someone say's "cookies" here.
```

## Crontab

Sometimes you'll run into situations where you want Slack messages to be sent periodically rather than in direct response to a keyword, for this Tangerine ships with a single-threaded Python implementation of Cron.

Let's pretend we want to send a message to everyone in a channel every five minutes, simply add the following to your mybot.py file:

```python
@tangerine.cron('*/5 * * * *')
def some_task():
    tangerine.speak("Hay Ride!", "#general")
```
