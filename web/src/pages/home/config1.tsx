import api from '~/api'
import { Config } from '~/api/data'
import { createForm } from "solform";

export default function Home() {
    const { register,setValue,getAllValues } = createForm<Config>();


    // let [config, setConfig] = createStore<Config>({
    //     phone: '',
    //     password: '',
    //     userId: 0,
    //     planId: '',
    //     enable: false,
    //     userAgent: '',
    //     longitude: 0,
    //     latitude: 0,
    //     address: '',
    //     desc: '',
    //     type: ''
    // })

    onMount(async () => {
        api.getStatus().then((res) => {
            console.log(res);
            setValue("enable",res.enable)
            setValue("phone",res.phone)
            setValue("password",res.password)
            setValue("userId",res.userId)
            setValue("planId",res.planId)
            setValue("userAgent",res.userAgent)
            setValue("longitude",res.longitude)
            setValue("latitude",res.latitude)
            setValue("address",res.address)
            setValue("desc",res.desc)
            setValue("type",res.type)
            // console.log(register);
            
        })

    })

    function save() {
        console.log(getAllValues());
    }

    return (
        <div>
            <div class="card w-full bg-base-100 shadow-xl">
                <div class="card-body">
                    <h2 class="card-title">修改配置</h2>
                    <div class="grid grid-cols-2 gap-2">
                        <label class="label cursor-pointer !justify-start gap-4">
                            <span class="label-text">是否启用</span>
                            <input type="checkbox" class="toggle" {...register("enable")} />
                        </label>
                        <label>
                        </label>
                        <label class="input-group">
                            <span>手机号</span>
                            <input type="text" class="input input-bordered" {...register("phone")} />
                        </label>
                        <label class="input-group">
                            <span>密码</span>
                            <input type="password" class="input input-bordered" {...register("password")} />
                        </label>
                        <label class="input-group">
                            <span>用户ID</span>
                            <input type="number" class="input input-bordered !appearance-none" {...register("userId")} />
                        </label>
                        <label class="input-group">
                            <span>计划ID</span>
                            <input type="text" class="input input-bordered" {...register("planId")} />
                        </label>
                        <label class="input-group">
                            <span>UA</span>
                            <input type="text" class="input input-bordered" {...register("userAgent")} />
                        </label>
                        <label class="input-group">
                            <span>经度</span>
                            <input type="tel" class="input input-bordered" {...register("longitude")} />
                        </label>
                        <label class="input-group">
                            <span>纬度</span>
                            <input type="tel" class="input input-bordered" {...register("latitude")} />
                        </label>
                        <label class="input-group">
                            <span>地址</span>
                            <input type="text" class="input input-bordered" {...register("desc")} />
                        </label>
                        <label class="input-group">
                            <span>描述</span>
                            <input type="text" class="input input-bordered" {...register("desc")} />
                        </label>
                        <label class="input-group">
                            <span>类型</span>
                            <input type="text" class="input input-bordered" {...register("type")} />
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