import * as base from './base'

const [
  host,
  gitUrl,
  branch,
  accessToken,
  methodName,
  requestStr,
] = process.argv.slice(2);

const request = JSON.parse(requestStr);

async function main() {
  const grpcObject = await base.init({ gitUrl, branch, accessToken });

  const response = await base.invoke({ host, grpcObject, methodName, request });

  return { methodName, request, response }
}

main()
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      console.log(err.message);
      process.exit(-1);
    });
