import { Link } from "solid-app-router";

export default function Home() {
    return (
        <div h-full>
            <header>
            </header>
            <div class="flex">
                <aside w-60>
                    <ul class="menu bg-base-100 w-56 p-2 rounded-box shadow-xl">
                        <li class="menu-title">
                            <span>Fuck 工学云</span>
                        </li>
                        <li>
                            <Link class="nav" href="/home">
                                主页
                            </Link>
                        </li>
                        <li>
                            <Link class="nav" href="/home/config">
                                打卡配置
                            </Link>
                        </li>
                        <li>
                            <Link class="nav" href="/home/logs">
                                打卡日志
                            </Link>
                        </li>
                    </ul>
                </aside>
                <main flex-auto>
                    <Outlet />
                </main>
            </div>
        </div>
    )
}