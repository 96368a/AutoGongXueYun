import { usePrefersDark } from '@solid-primitives/media'
import { createStorageSignal } from '@solid-primitives/storage'

export default function useDark() {
  const prefersDark = usePrefersDark()
  const [value, setValue] = createStorageSignal<string>('color-mode', 'auto', { api: localStorage })
  const isDark = createMemo(() => value() === 'auto' ? prefersDark() : value() === 'dark')

  createEffect(() => document.documentElement.classList.toggle('dark', isDark()))
  const toggle = () => setValue(isDark() ? 'light' : 'dark')

  return {
    isDark,
    toggle,
  }
}
