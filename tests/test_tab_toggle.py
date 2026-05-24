import asyncio
from textual.app import App
from lastcode.app import VisualizerScreen
from lastcode.problems import reverse_linked_list

class TestApp(App):
    def on_mount(self) -> None:
        self.push_screen(VisualizerScreen(reverse_linked_list))

async def test_tab_toggle():
    app = TestApp()
    async with app.run_test() as pilot:
        # Wait for the screen to mount
        await pilot.pause()
        
        screen = app.screen
        assert isinstance(screen, VisualizerScreen), f"Expected VisualizerScreen, got {type(screen)}"
        
        # Get TabbedContent
        tabs = screen.query_one("#code-tabs")
        
        # Initially, Solution tab should be active
        assert tabs.active == "solution-tab", f"Expected active tab solution-tab, got {tabs.active}"
        assert screen.query_one("#left-panel").border_title == "solution", f"Expected border title 'solution', got {screen.query_one('#left-panel').border_title!r}"
        assert screen._step == 0, f"Expected initial step 0, got {screen._step}"
        
        # Verify that heights have not collapsed
        switcher = tabs.query_one("ContentSwitcher")
        active_pane = tabs.active_pane
        assert switcher.size.height > 1, f"ContentSwitcher collapsed! Height was {switcher.size.height}"
        assert active_pane.size.height > 1, f"TabPane collapsed! Height was {active_pane.size.height}"
        
        # Press right arrow key to step visualizer
        await pilot.press("right")
        await pilot.pause()
        
        # Verify tab did not change, but screen step incremented
        assert tabs.active == "solution-tab", f"Tab incorrectly switched on right arrow key, got {tabs.active}"
        assert screen._step == 1, f"Expected visualizer step to increment to 1, got {screen._step}"
        
        # Press Tab to toggle to Problem
        await pilot.press("tab")
        await pilot.pause()
        
        assert tabs.active == "problem-tab", f"Expected active tab problem-tab after pressing tab, got {tabs.active}"
        assert screen.query_one("#left-panel").border_title == "problem", f"Expected border title 'problem' after pressing tab, got {screen.query_one('#left-panel').border_title!r}"
        
        # Press left arrow key to step visualizer back
        await pilot.press("left")
        await pilot.pause()
        
        # Verify tab did not change, but screen step decremented
        assert tabs.active == "problem-tab", f"Tab incorrectly switched on left arrow key, got {tabs.active}"
        assert screen._step == 0, f"Expected visualizer step to decrement to 0, got {screen._step}"
        
        # Press Tab again to toggle back to Solution
        await pilot.press("tab")
        await pilot.pause()
        
        assert tabs.active == "solution-tab", f"Expected active tab solution-tab after pressing tab twice, got {tabs.active}"
        assert screen.query_one("#left-panel").border_title == "solution", f"Expected border title 'solution' after pressing tab twice, got {screen.query_one('#left-panel').border_title!r}"
        
        print("SUCCESS: Tab toggle integration test passed successfully!")

if __name__ == "__main__":
    asyncio.run(test_tab_toggle())
