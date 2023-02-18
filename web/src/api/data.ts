export interface Config {
  phone: string
  password: string
  userId: string
  planId: string
  enable: boolean
  userAgent: string
  longitude: string
  latitude: string
  country: string
  province: string
  city: string
  area: string
  address: string
  desc: string
  type: string
  plusplusKey: string
  serverChanKey: string
  [key: string]: any
}

export interface Plan {
  planId: string
  planName: string
}

export interface Empty {
  [key: string]: any
}
