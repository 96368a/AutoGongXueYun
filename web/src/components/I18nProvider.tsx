import type { ParentComponent } from 'solid-js'
import { I18nContext, createI18nContext } from '@solid-primitives/i18n'

export const I18nProvider: ParentComponent<{
  dict?: Record<string, Record<string, any>>
  locale?: string
}> = (props) => {
  const value = createI18nContext(props.dict, props.locale)
  return (
    <I18nContext.Provider value={value}>
      {props.children}
    </I18nContext.Provider>
  )
}
