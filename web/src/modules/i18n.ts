export const dict = Object.fromEntries(
  Object.entries(
    import.meta.glob('../../locales/*.y(a)?ml', { eager: true }))
    .map(([key, value]: [string, any]) => {
      const yaml = key.endsWith('.yaml')
      return [key.slice(14, yaml ? -5 : -4), value.default]
    }),
)

export const availableLocales = Object.keys(dict)
