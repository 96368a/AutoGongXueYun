import api from "~/api"

export default function Index() {
  const [name, setName] = createSignal('')

  const [t] = useI18n()

  const navigate = useNavigate()
  const go = () => {
    if (name())
      navigate(`/hi/${encodeURIComponent(name())}`)
  }

  onMount(async () => {
    api.loginCheck().then((res) => {
      console.log(res)
    })
  });

  return (
    <div>
      <div class="i-carbon-campsite text-4xl inline-block" />
      <p>
        <a rel="noreferrer" href="https://github.com/antfu/vitesse-lite" target="_blank">
          Vitesse Lite
        </a>
      </p>
      <p>
        <em class="text-sm op75">{t('intro.desc')}</em>
      </p>

      <div class="py-4" />

      <input
        onInput={e => setName(e.currentTarget.value)}
        id="input"
        placeholder={t('intro.whats-your-name')}
        aria-label={t('intro.whats-your-name')}
        type="text"
        class="px-4 py-2 w-250px text-center bg-transparent outline-none outline-active:none border border-rounded border-gray-200 border-dark:gray-700"
        onKeyDown={({ key }) => key === 'Enter' && go()}
      />

      <div>
        <button
          class="m-3 text-sm btn"
          disabled={!name()}
          onClick={go}
        >
          {t('button.go')}
        </button>
      </div>
    </div>
  )
}
