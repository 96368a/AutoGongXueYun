import api from '~/api'
import { Config, Empty } from '~/api/data'

export default function Home() {

    let defaultConfig: Config
    let [config, setConfig] = createStore<Config>({
        phone: '',
        password: '',
        userId: '',
        planId: '',
        enable: false,
        userAgent: '',
        country: '',
        province: '',
        city: '',
        area: '',
        longitude: '',
        latitude: '',
        address: '',
        desc: '',
        type: '',
        plusplusKey: '',
        serverChanKey: '',
    })

    const [plans, setPlans] = createSignal([])

    function initData() {
        api.getConfig().then((res) => {
            // 初始化配置
            setConfig(res)
            defaultConfig = res
        })
        api.getPlans().then((res) => {
            // console.log(res);
            setPlans(res)
        })
    }

    onMount(async () => {
        initData()
    })

    function save() {
        let data: Empty = {}
        for (const key in config) {
            if (config[key] != defaultConfig[key]) {
                data[key] = config[key]
            }
        }
        console.log(data);
        api.saveConfig(data).then((res) => {
            alert(res.msg)
            initData()
        })
    }

    const handleGetLocation = () => {
        if (config.latitude && config.longitude) {
            api.getLocations(config.latitude + "," + config.longitude).then((res) => {
                console.log(res);
                if (res.code == 200 && res.data.length > 0) {
                    setConfig('country', res.data[0].country)
                    setConfig('province', res.data[0].province)
                    setConfig('city', res.data[0].city)
                    setConfig('area', res.data[0].area)
                    const address = `${res.data[0].province} · ${res.data[0].city} · ${res.data[0].area} · ${res.data[0].name}`
                    setConfig('address', address)
                } else {
                    setConfig('address', '获取地址失败')
                }
            })
        } else {
            alert('请先填写经纬度')
        }
    }

    return (
        <div>
            <div class="card w-full bg-base-100 shadow-xl">
                <div class="card-body">
                    <h2 class="card-title">修改配置</h2>
                    <div class="divider"></div>
                    <div>
                        <label class="label cursor-pointer !justify-start gap-4">
                            <span class="label-text">是否启用</span>
                            <input type="checkbox" class="toggle" checked={config.enable} onChange={e => setConfig('enable', e.currentTarget.checked)} />
                        </label>
                    </div>
                    <div class="divider"></div>
                    <div class="grid grid-cols-2 gap-2">
                        <label class="input-group">
                            <span>手机号</span>
                            <input type="text" class="input input-bordered" value={config.phone} oninput={e => setConfig('phone', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>密码</span>
                            <input type="password" class="input input-bordered" value={config.password} oninput={e => setConfig('password', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>实习计划</span>
                            <select class="select select-bordered w-full max-w-xs" value={config.planId} onChange={e => setConfig('planId', e.currentTarget.value)}>
                                <option selected={config.planId==''} value="">请选择实习计划</option>
                                <For each={plans()}>
                                    {plan => <option selected={plan.planId==config.planId} value={plan.planId}>{plan.planName}</option>}
                                </For>
                            </select>
                            {/* <input type="text" class="input input-bordered" value={config.planId} oninput={e => setConfig('planId', e.currentTarget.value)} /> */}
                        </label>
                    </div>
                    <div class="divider"></div>
                    <div class="flex flex-col gap-2">
                        <div class='flex'>
                            <label class="input-group">
                                <span>经度</span>
                                <input type="tel" class="input input-bordered" value={config.longitude} oninput={e => setConfig('longitude', e.currentTarget.value)} />
                            </label>
                            <label class="input-group">
                                <span>纬度</span>
                                <input type="tel" class="input input-bordered" value={config.latitude} oninput={e => setConfig('latitude', e.currentTarget.value)} />
                            </label>
                        </div>
                        <div class="flex">
                            <label class="input-group !w-auto">
                                <span>地址</span>
                                <input type="text" class="input input-bordered min-w-100" value={config.address} oninput={e => setConfig('address', e.currentTarget.value)} />
                            </label>
                            <label class="flex items-center px-2 mx-2">
                                <button class="btn btn-outline btn-info btn-xs" onclick={handleGetLocation}>获取地址</button>
                            </label>
                        </div>
                        <label class="input-group">
                            <span>类型</span>
                            <select class="select select-bordered w-full max-w-xs" value={config.type} onCanPlay={e => setConfig('type', e.currentTarget.value)}>
                                <option selected value="android">android</option>
                                <option selected value="ios">ios</option>
                                <option selected value="web">web</option>
                            </select>
                        </label>
                    </div>
                    <div class="divider"></div>
                    <div class="flex flex-col gap-2">
                        <label class="input-group">
                            <span>plusplus推送key</span>
                            <input type="text" class="input input-bordered" value={config.plusplusKey} oninput={e => setConfig('plusplusKey', e.currentTarget.value)} />
                        </label>
                        <label class="input-group">
                            <span>server酱推送key</span>
                            <input type="text" class="input input-bordered" value={config.serverChanKey} oninput={e => setConfig('serverChanKey', e.currentTarget.value)} />
                        </label>
                    </div>
                    <div class="divider"></div>
                    <div class="card-actions justify-start">
                        <button class="btn btn-primary" onclick={save}>保存</button>
                    </div>
                </div>
            </div>
        </div>
    )
}