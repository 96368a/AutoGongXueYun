import api from '~/api'

export default function Index() {
  // const [t] = useI18n()

  const navigate = useNavigate()

  onMount(async () => {
    api.loginCheck().then((res) => {
      console.log(res)

      if (res === false)
        navigate('/login')
      else
        navigate('/home')
    })
  })

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
            <li><a>Item 1</a></li>
            <li><a>Item 2</a></li>
            <li class="menu-title">
              <span>Category</span>
            </li>
            <li><a>Item 1</a></li>
            <li><a>Item 2</a></li>
          </ul>
        </aside>
        <main flex-auto>
          <div class="card w-full bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title">修改配置</h2>
              <div class="grid grid-cols-2 gap-2">
                <label class="label cursor-pointer !justify-start gap-4">
                  <span class="label-text">是否启用</span>
                  <input type="checkbox" class="toggle" />
                </label>
                <label>
                </label>
                <label class="input-group">
                  <span>手机号</span>
                  <input type="text" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>密码</span>
                  <input type="password" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>用户ID</span>
                  <input type="text" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>计划ID</span>
                  <input type="text" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>UA</span>
                  <input type="text" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>经度</span>
                  <input type="text" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>纬度</span>
                  <input type="text" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>地址</span>
                  <input type="text" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>描述</span>
                  <input type="text" class="input input-bordered" />
                </label>
                <label class="input-group">
                  <span>类型</span>
                  <input type="text" class="input input-bordered" />
                </label>
              </div>

              <div class="card-actions justify-start">
                <button class="btn btn-primary">保存</button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
