import os
import json
import pathlib
import typer

from gpt_engineer.chat_to_files import to_files
from gpt_engineer.ai import AI
from gpt_engineer.steps import STEPS
from gpt_engineer.db import DB, DBs


app = typer.Typer()


@app.command()
def chat(
    project_path: str = typer.Argument(str(pathlib.Path(os.path.curdir) / "example"), help="path"),
    run_prefix: str = typer.Option(
        "",
        help="run prefix, if you want to run multiple variants of the same project and later compare them",
    ),
    model: str = "gpt-4",
    temperature: float = 0.1,
):
    if project_path is None:
        project_path = str(pathlib.Path(__file__).parent / "example")
    
    input_path = project_path
    memory_path = pathlib.Path(project_path) / (run_prefix + "memory")
    workspace_path = pathlib.Path(project_path) / (run_prefix + "workspace")

    ai = AI(
        model=model,
        temperature=temperature,
    )

    dbs = DBs(
        memory=DB(memory_path),
        logs=DB(pathlib.Path(memory_path) / "logs"),
        input=DB(input_path),
        workspace=DB(workspace_path),
        identity=DB(pathlib.Path(__file__).parent / "identity"),
    )

    for step in STEPS:
        messages = step(ai, dbs)
        dbs.logs[step.__name__] = json.dumps(messages)


def execute():
    app()


if __name__ == "__main__":
    execute()