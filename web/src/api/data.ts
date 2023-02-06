export interface Config {
    phone: string
    password: string
    userId: string
    planId: string
    enable: boolean
    userAgent: string
    longitude: string
    latitude: string
    address: string
    desc: string
    type: string
    plusplusKey: string
    serverChanKey: string
    [key: string]: any
}

export interface Empty {
    [key: string]: any
}