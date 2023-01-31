import api from '~/api'
import { Config } from '~/api/data'

export default function Home() {

    let [config, setConfig] = createStore<Config>({
        phone: '',
        password: '',
        userId: 0,
        planId: '',
        enable: false,
        userAgent: '',
        longitude: 0,
        latitude: 0,
        address: '',
        desc: '',
        type: ''
    })

    onMount(async () => {
        api.getStatus().then((res) => {
            console.log(res);
            setConfig(res.data)
        })

    })

    function save() {
        console.log(config);
    }

    return (
        <div>
            <div class="card w-full bg-base-100 shadow-xl">
                <div class="card-body">
                    <h2 class="card-title">修改配置</h2>
                    <div class="grid grid-cols-2 gap-2">
                        <label class="label cursor-pointer !justify-start gap-4">
                            <span class="label-text">是否启用</span>
                            <input type="checkbox" class="toggle" checked={config.enable} onChange={e => setConfig('enable', e.currentTarget.checked)} />
                        </label>
                        <label>
                        </label>
                        <label class="input-group">
                            <span>手机号</span>
                            <input type="text" class="input input-bordered" value={config.phone} oninput={e => setConfig('phone', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>密码</span>
                            <input type="password" class="input input-bordered" value={config.password} oninput={e => setConfig('password', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>用户ID</span>
                            <input type="tel" class="input input-bordered" value={config.userId} oninput={e => setConfig('userId', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>计划ID</span>
                            <input type="text" class="input input-bordered" value={config.planId} oninput={e => setConfig('planId', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>UA</span>
                            <input type="text" class="input input-bordered" value={config.userAgent} oninput={e => setConfig('userAgent', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>经度</span>
                            <input type="tel" class="input input-bordered" value={config.longitude} oninput={e => setConfig('longitude', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>纬度</span>
                            <input type="tel" class="input input-bordered" value={config.latitude} oninput={e => setConfig('latitude', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>地址</span>
                            <input type="text" class="input input-bordered" value={config.address} oninput={e => setConfig('address', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>描述</span>
                            <input type="text" class="input input-bordered" value={config.desc} oninput={e => setConfig('desc', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>类型</span>
                            <input type="text" class="input input-bordered" value={config.type} oninput={e => setConfig('type', e.currentTarget.value)} />
                        </label>
                    </div>
                    <div class="card-actions justify-start">
                        <button class="btn btn-primary" onclick={save}>保存</button>
                    </div>
                </div>
            </div>
        </div>
    )
}