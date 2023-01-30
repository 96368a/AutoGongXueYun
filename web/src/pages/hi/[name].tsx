export default function Hi() {
  const navigate = useNavigate()
  const { name } = useParams<{ name: string }>()

  const [t] = useI18n()

  return (
    <div>
      <div class="i-carbon-pedestrian text-4xl inline-block" />
      <p>
        {t('intro.hi', { name })}
      </p>
      <p class="text-sm op50">
        <em>{t('intro.dynamic-route')}</em>
      </p>

      <div>
        <button
          class="btn m-3 text-sm mt-8"
          onClick={() => navigate(-1)}
        >
          {t('button.back')}
        </button>
      </div>
    </div>
  )
}
