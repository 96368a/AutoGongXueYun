/// <reference types="vitest" />

import path from 'path'
import { defineConfig } from 'vite'
import Solid from 'vite-plugin-solid'
import Pages from 'vite-plugin-pages'
// import YamlImport from 'vite-plugin-yaml2'
import pluginYaml from "vite-plugin-yaml2";
import AutoImport from 'unplugin-auto-import/vite'
import Unocss from 'unocss/vite'

import devtools from 'solid-devtools/vite'

export default defineConfig({
  resolve: {
    alias: {
      '~/': `${path.resolve(__dirname, 'src')}/`,
    },
    conditions: ['development', 'browser'],
  },
  plugins: [
    // https://github.com/antfu/unocss
    // see unocss.config.ts for config
    Unocss(),
    devtools({
      locator: {
        targetIDE: 'vscode',
        componentLocation: true,
        jsxLocation: true,
      },
      autoname: true, // e.g. enable autoname
    }),
    Solid(),

    // https://github.com/hannoeru/vite-plugin-pages
    Pages(),

    // https://github.com/antfu/unplugin-auto-import
    AutoImport({
      imports: [
        'solid-js',
        'solid-app-router',
        { '@solid-primitives/i18n': ['useI18n'] },
      ],
      dts: 'src/auto-imports.d.ts',
      dirs: [
        'src/primitives',
      ],
    }),

    pluginYaml(),
  ],

  // https://github.com/vitest-dev/vitest
  test: {
    environment: 'jsdom',
    transformMode: {
      web: [/\.[jt]sx?$/],
    },
    deps: {
      inline: [
        /solid-testing-library/,
        /solid-js/,
      ],
    },
  },
})
