export default {
  expo: {
    name: 'Devi Jewellers',
    slug: 'devi-jewellers-owner',
    version: '1.0.1',
    orientation: 'portrait',
    userInterfaceStyle: 'light',
    icon: './assets/icon.png',
    android: {
      package: 'in.devijewellers.owner',
      versionCode: 6,
      googleServicesFile: process.env.GOOGLE_SERVICES_JSON || './google-services.json',
      usesCleartextTraffic: process.env.DEVI_LOCAL_TEST === '1',
      adaptiveIcon: {
        foregroundImage: './assets/adaptive-icon.png',
        backgroundColor: '#000000',
      },
    },
    web: {
      favicon: './assets/favicon.png',
    },
    plugins: [
      'expo-secure-store',
      'expo-sharing',
      ['expo-notifications', { defaultChannel: 'customer-payments', enableBackgroundRemoteNotifications: false }],
      [
        './plugins/withNetworkPolicy.cjs',
        { allowLocal: process.env.DEVI_LOCAL_TEST === '1' },
      ],
    ],
    extra: {
      apiUrl: process.env.EXPO_PUBLIC_API_URL || '',
      eas: { projectId: process.env.EAS_PROJECT_ID || '992a3ef1-36cb-4b6a-88d3-7698e900e7ad' },
    },
  },
};
