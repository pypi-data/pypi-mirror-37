import os
import re
import sys
import click
import gitlab


@click.command()
@click.option('--token', default=os.environ.get("PRIVATE_TOKEN"), type=str, help='Gitlab auth token')
@click.option('--label', default="tested", type=str, help='Gitlab label name to check for')
@click.option('--project-id', default=os.environ.get("CI_PROJECT_ID"), type=str, help='Gitlab project id')
@click.option('--commit-hash', default=os.environ.get("CI_COMMIT_SHA"), type=str, help='Git commit reference')
def mr_tested(token, label, project_id, commit_hash):

    gl = gitlab.Gitlab('https://gitlab.pi.planetinnovation.com.au', private_token=token)
    gl.auth()

    project = gl.projects.get(project_id, lazy=True)
    commit = project.commits.get(commit_hash)

    mrs = commit.merge_requests()
    is_tested = len(mrs) > 0

    print("""
    --------------
    Merge Requests
    --------------""")
    for mr in mrs:
        tested = label in mr['labels']
        str_tested = " (tested)" if tested else " (NOT tested)"
        is_tested &= tested

        if tested:
            found_instructions = False
            pmr = project.mergerequests.get(mr['iid'], lazy=True)
            for note in pmr.notes.list(all=True):
                if re.match(f"(^|\W)~{label}\W", note.body):
                    found_instructions = True

            if not found_instructions:
                is_tested = False
                str_tested = "\n> ERROR: test instructions missing, please add '~tested' to MR comment with instructions\n"
        print(f"* !{mr['iid']}: {mr['title']} {str_tested}")

    sys.exit(0 if is_tested else 1)


if __name__ == '__main__':
    mr_tested()
