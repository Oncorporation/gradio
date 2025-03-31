from __future__ import annotations

from gradio_client.documentation import document

from gradio.blocks import BlockContext
from gradio.component_meta import ComponentMeta
from gradio.events import Events
from gradio.i18n import I18nData


class Tabs(BlockContext, metaclass=ComponentMeta):
    """
    Tabs is a layout element within Blocks that can contain multiple "Tab" Components.
    """

    EVENTS = [Events.change, Events.select]

    def __init__(
        self,
        *,
        selected: int | str | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = None,
        sort_order: list[int | str] | None = None,
    ):
        """
        Parameters:
            selected: The currently selected tab. Must correspond to an id passed to the one of the child TabItems. Defaults to the first TabItem.
            visible: If False, Tabs will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional string or list of strings that are assigned as the class of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, this layout will not be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: in a gr.render, Components with the same key across re-renders are treated as the same component, not a new component. Properties set in 'preserved_by_key' are not reset across a re-render.
            preserved_by_key: A list of parameters from this component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key, these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an event listener) instead of re-rendered based on the values provided during constructor.
            sort_order: Optional list of identifiers (e.g. child Tab._id values) determining the order in which the tabs appear in the parent Tabs component. Lower values appear earlier. If not provided, tabs are shown in the order they were created.
        """
        BlockContext.__init__(
            self,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
        )
        self.selected = selected
        self.sort_order = sort_order

    def sort_tabs(self):
        """
        Sort child tabs based on their sort_order attribute.
        This is called automatically when all tabs have been added to the Tabs component.
        """
        if self.sort_order is not None:
            # If parent Tabs has an explicit sort_order list, rearrange tabs according to it
            sorted_children = []
            remaining_children = self.children.copy()

            # First add the tabs in the specified sort order
            for tab_id in self.sort_order:
                for i, child in enumerate(remaining_children):
                    if isinstance(child, Tab) and child._id == tab_id:
                        sorted_children.append(child)
                        remaining_children.pop(i)
                        break

            # Then add any remaining tabs that weren't in the explicit sort_order
            sorted_children.extend(remaining_children)
            self.children = sorted_children
        else:
            # Otherwise sort tabs based on their individual sort_order values
            tab_children = [child for child in self.children if isinstance(child, Tab)]
            non_tab_children = [
                child for child in self.children if not isinstance(child, Tab)
            ]

            # Sort only the Tab children based on their sort_order
            tab_children.sort(
                key=lambda tab: float("inf")
                if tab.sort_order is None
                else tab.sort_order
            )

            # Combine them back together
            self.children = tab_children + non_tab_children


@document()
class Tab(BlockContext, metaclass=ComponentMeta):
    """
    Tab (or its alias TabItem) is a layout element. Components defined within the Tab will be visible when this tab is selected tab.
    Example:
    with gr.Blocks() as demo:
        with gr.Tabs():
            with gr.Tab("Lion", sort_order=3):
                gr.Image("lion.jpg")
            with gr.Tab("Tiger", sort_order=1):
                gr.Image("tiger.jpg")
            with gr.Tab("Cheetah", sort_order=2):
                gr.Image(cheetah1.jpg")

        with gr.Tabs() as tabs:
            with gr.Tab("Lion") as tab1:
                gr.Image("lion.jpg")
            with gr.Tab("Tiger") as tab2:
                gr.Image("tiger.jpg")
            with gr.Tab("Cheetah") as tab3:
                gr.Image("cheetah1.jpg")
            gr.update(sort_order=[tab2._id, tab1._id, tab3._id])

    Guides: controlling-layout
    """

    EVENTS = [Events.select]

    def __init__(
        self,
        label: str | I18nData | None = None,
        visible: bool = True,
        interactive: bool = True,
        *,
        id: int | str | None = None,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        scale: int | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = None,
        sort_order: int | None = None,
    ):
        """
        Parameters:
            label: The visual label for the tab
            id: An optional identifier for the tab, required if you wish to control the selected tab from a predict function.
            elem_id: An optional string that is assigned as the id of the <div> containing the contents of the Tab layout. The same string followed by "-button" is attached to the Tab button. Can be used for targeting CSS styles.
            elem_classes: An optional string or list of strings that are assigned as the class of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, this layout will not be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            scale: relative size compared to adjacent elements. 1 or greater indicates the Tab will expand in size.
            visible: If False, Tab will be hidden.
            interactive: If False, Tab will not be clickable.
            sort_order: Optional integer determining the order in which the tab appears in its parent Tabs component. Lower values appear earlier. If not provided, tabs are shown in the order they were created.
        """
        BlockContext.__init__(
            self,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
        )
        self.label = label
        self.id = id
        self.visible = visible
        self.scale = scale
        self.interactive = interactive
        self.sort_order = sort_order

    def get_expected_parent(self) -> type[Tabs]:
        return Tabs

    def get_block_name(self):
        return "tabitem"

    def add_to_tabgroup(self, parent: Tabs) -> None:
        """
        Add this tab to a parent Tabs component with proper ordering.
        Called internally by the Tabs component when the tab is added.
        """
        # If the parent has a sort_order list, use that to determine this tab's position
        if parent.sort_order is not None:
            # Add this Tab to the parent's children list at the position specified by sort_order
            order = self.sort_order if self.sort_order is not None else float("inf")

            # Insert tab in the right position based on sort_order
            # Find the position where this tab should be inserted
            i = 0
            for i, child in enumerate(parent.children):
                if isinstance(child, Tab):
                    child_order = getattr(child, "sort_order", float("inf"))
                    if order < child_order:
                        break
            else:
                i = len(parent.children)  # Insert at end if no suitable position found

            # Insert tab at position i
            parent.children.insert(i, self)
        else:
            # Default behavior: append to the end
            parent.children.append(self)


TabItem = Tab
