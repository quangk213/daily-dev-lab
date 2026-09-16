export default function SidebarItem({ name }: { name: string }) {
  return (
    <li className="px-1 py-4 border-y border-lime-400 capitalize hover:bg-amber-300 hover:text-black cursor-pointer">
      {name}
    </li>
  );
}
