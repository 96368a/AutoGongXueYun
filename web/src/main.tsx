import App from './App'
import { dict } from './modules/i18n'


import '@unocss/reset/tailwind.css'
import '~/styles/main.css'
import 'uno.css'
import '@kidonng/daisyui/index.css';
import { I18nProvider } from '~/components/I18nProvider'
// import { HopeProvider } from '@hope-ui/solid'

render(
  () => ( 
    <I18nProvider dict={dict} locale="zh-CN">
      {/* <HopeProvider> */}
        <App />
        {/* </HopeProvider> */}
    </I18nProvider>
  ),
  document.getElementById('root')!,
)
