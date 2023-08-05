import * as fs from 'fs';
import * as base from './base';
import { ICase, ICases } from "./types";
import { DiffPatcher, formatters } from 'jsondiffpatch';

const [
  host,
  gitUrl,
  branch,
  accessToken,
  caseFilePath,
  caseName,
] = process.argv.slice(2);

interface IDiff {
  methodName: string;
  caseName?: string;
  html?: string;
  delta: any;
}

const cssText = fs.readFileSync(require.resolve('jsondiffpatch/dist/formatters-styles/html.css'));

async function main(): Promise<IDiff[]> {
  if (!fs.existsSync(caseFilePath)) {
    throw new Error(`Cases file not exists: ${caseFilePath}`);
  }

  const cases: ICases = require(caseFilePath);

  const grpcObject = await base.init({ gitUrl, branch, accessToken });

  let casesArr: ICase[] = [];
  if (Array.isArray(cases.cases)) {
    casesArr = cases.cases;
  } else {
    Object.keys(cases.cases).forEach((key) => {
      casesArr.push({
        ...((cases.cases as any)[key]),
        name: key,
      });
    });
  }

  if (caseName) {
    casesArr = casesArr.filter(item => item.name === caseName);
  }

  return await Promise.all(casesArr.map(async (item) => {
    const responseRes = await base.invoke({
      host,
      grpcObject,
      methodName: item.id,
      request: item.request,
    });
    const diffPatcher = new DiffPatcher();
    const delta = diffPatcher.diff(responseRes, item.response);
    if (delta) {
      return {
        methodName: item.id,
        caseName: item.name,
        delta,
        html: formatters.html.format(delta, responseRes)
      };
    }
    return {
      methodName: item.id,
      delta,
      caseName: item.name,
      html: '',
    };
  }));
}

main()
    .then((res) => {
      const hasDiff = res
          .filter(item => !!item.delta);
      const html = `<h2>Success/Total: ${res.length - hasDiff.length}/${res.length}</h2>` + res
          .map((item) => {
            return `<h3>${item.methodName}   ${item.caseName}</h3>` +
                `<p>${item.delta ? `<span class="label fail">FAIL</span> 详情: ` : `<span class="label pass">PASS</span>`}</p>` +
                `${item.html}`;
          })
          .join('');
      console.log(`<style>${cssText}</style>${html}`);
      if (hasDiff.length > 0) {
        process.exit(2);
      }
    })
    .catch((err) => {
      console.log(err.message);
      process.exit(1);
    });
