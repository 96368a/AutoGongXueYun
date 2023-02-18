import api from '~/api'

export default function Login() {
  const [phone, setPhone] = createSignal('17666666666')
  const [password, setPassword] = createSignal('pass@word')

  function loginHandle() {
    if (phone() === '' || password() === '') {
      alert('手机号或密码不能为空')
      return
    }
    if (phone().length !== 11 || !/^1\d{10}$/.test(phone())) {
      alert('手机号格式不正确')
      return
    }
    if (password().length < 6) {
      alert('密码长度不能小于6位')
      return
    }
    api.login(phone(), password()).then((res) => {
      if (res.code === 200) {
        alert('登录成功')
        localStorage.setItem('token', res.token)
        location.href = '/'
      }
      else {
        alert(res.msg)
      }
    })
    console.log(phone(), ':', password())
  }

  return (
        <div class="flex justify-center">
            <div class="card w-96 bg-base-100 shadow-xl">
                <div class="card-body text-center items-center">
                    <h2 class="card-title">欢迎登录</h2>
                    <div class="form-control">
                        <label class="input-group">
                            <span>手机号</span>
                            <input type="text" placeholder="17666666666" class="input input-bordered" value={phone()} onchange={e => setPhone(e.currentTarget.value)} maxlength="11"/>
                        </label>
                    </div>
                    <div class="form-control">
                        <label class="input-group">
                            <span>密码</span>
                            <input type="password" placeholder="p@ssw0rd" class="input input-bordered" value={password()} onchange={e => setPassword(e.currentTarget.value)} maxlength="20"/>
                        </label>
                    </div>
                    <div class="flex">
                        <button class="btn btn-primary w-40" onclick={loginHandle}>登录</button>
                    </div>
                </div>
            </div>

        </div >)
}
