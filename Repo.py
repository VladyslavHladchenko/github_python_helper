import git
import os
import socket
import colorama

class Repo:
  """clones to local dir"""

  def __init__(self,repo_name,user,token):
    folder = repo_name.split('/')[1]

    self.host = 'colab' if 'COLAB_RELEASE_TAG' in os.environ else socket.gethostname()
    if os.path.exists(folder):
      self.repo = git.Repo(folder)
    else:
      self.repo = git.Repo.clone_from(f"https://{user}:{token}@github.com/{repo_name}.git", to_path=folder)

  def pull(self):
    self.repo.remote(name='origin').pull()

  def push(self, commit_message = ''):
    self.diff

    print('confirm push by typing "yes"...')
    if input() != 'yes':
      print('push cancelled')
      return
    print('overwrite the commit message (leave blank to skip)')
    new_msg = input()
    if new_msg != '':
      commit_message = new_msg

    commit_message = commit_message + f" -- from {self.host}"
    self.repo.git.add(all=True)
    self.repo.index.commit(commit_message)

    push_result = self.repo.remote(name='origin').push()
    print('pushed.',**push_result)

  @property
  def diff(self):
    for line in self.repo.git.diff().split('\n'):
        if line.startswith('+'):
            print(colorama.Fore.GREEN,end='')
        if line.startswith('-'):
            print(colorama.Fore.RED,end='')
        print(line)
        print(colorama.Style.RESET_ALL,end='')