from pathlib import Path

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.events import Mount
from textual.widgets import Tree
from textual.widgets._tree import TreeNode

from note_app.domain.folder import Folder
from note_app.repositories.base_folder_repository import BaseFolderRepository


class FileTreeWidget(VerticalScroll):
    _tree: Tree
    _folder_repo: BaseFolderRepository
    _root_path: Path

    def __init__(
        self,
        folder_repo: BaseFolderRepository,
        root_path: Path,
        *args,
        **kwargs,
    ) -> None:
        self._folder_repo = folder_repo
        self._root_path = root_path
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        self._tree = Tree("Notices")
        yield self._tree

    def _on_mount(self, event: Mount) -> None:
        root = self.query_one(Tree).root
        root.data = Folder(self._root_path.name or "root", self._root_path)
        root.expand()

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node: TreeNode[Folder] = event.node
        if node.data is None:
            return
        node.remove_children()
        folders = self._folder_repo.get_folder_by_path(node.data.path)
        for folder in folders:
            node.add(folder.name, folder)
