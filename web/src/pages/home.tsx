import { Router, Routes, Route, Link } from "solid-app-router";

export default function Home() {
    return (
        <div h-full>
            <header>
            </header>
            <div class="flex">
                <aside w-60>
                    <ul class="menu bg-base-100 w-56 p-2 rounded-box shadow-xl">
                        <li class="menu-title">
                            <span>Category</span>
                        </li>
                        <li>
                            <Link class="nav" href="/home/config">
                                Home
                            </Link>
                        </li>
                        <li><a>Item 2</a></li>
                        <li class="menu-title">
                            <span>Category</span>
                        </li>
                        <li><a>Item 1</a></li>
                        <li><a>Item 2</a></li>
                    </ul>
                </aside>
                <main flex-auto>
                    <Outlet />
                </main>
            </div>
        </div>
    )
}