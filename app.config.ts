export default {
  expo: {
    name: 'Devi Jewellers',
    slug: 'devi-jewellers-owner',
    version: '1.0.0',
    orientation: 'portrait',
    userInterfaceStyle: 'light',
    icon: './assets/icon.png',
    android: {
      package: 'in.devijewellers.owner',
      versionCode: 1,
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
    },
  },
};
