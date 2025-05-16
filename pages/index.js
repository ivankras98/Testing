export default function Home() {
  return (
    <div>
      <h1>Добро пожаловать</h1>
    </div>
  );
}

export async function getServerSideProps(context) {
  const isAuthenticated = false; // Замените на реальную проверку сессии (например, через next-auth)
  if (!isAuthenticated) {
    return {
      redirect: {
        destination: '/authentication',
        permanent: false,
      },
    };
  }
  return { props: {} };
}