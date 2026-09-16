import "./App.css";
import SidebarItem from "./SidebarItem";

function App() {
  return (
    <div className="h-screen grid grid-cols-[300px_1fr]">
      <aside className="h-full bg-black flex flex-col overflow-y-auto no-scrollbar">
        <div className="sticky top-0 bg-black px-1 py-4 border-b text-lime-400 text-3xl font-semibold">
          <h1>SHOPI</h1>
        </div>
        <ul className="mt-4 text-lime-400">
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 2" />
          <SidebarItem name="Item 3" />
          <SidebarItem name="Item 4" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
          <SidebarItem name="Item 1" />
        </ul>
      </aside>
      <main></main>
    </div>
  );
}

export default App;
