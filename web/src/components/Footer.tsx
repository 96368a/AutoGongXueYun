import { availableLocales as locales } from '~/modules/i18n'

export default function Footer() {
  const { toggle } = useDark()

  const [t, { locale }] = useI18n()

  const toggleLocales = () => {
    locale(locales[(locales.indexOf(locale()) + 1) % locales.length])
  }

  return (
    <nav class="text-xl mt-6 inline-flex gap-2">
      <button class="icon-btn !outline-none" title={t('button.toggle_dark')} onClick={toggle}>
        <div class='i-carbon-sun dark:i-carbon-moon' />
      </button>

      <a class="icon-btn mx-2" title={t('button.toggle_langs')} onClick={toggleLocales}>
        <div i-carbon-language />
      </a>

      <a
        class="icon-btn i-carbon-logo-github"
        rel="noreferrer"
        href="https://github.com/antfu/vitesse-lite"
        target="_blank"
        title="GitHub"
      />
    </nav>

  )
}
