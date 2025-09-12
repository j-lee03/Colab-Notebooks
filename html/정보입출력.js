const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log("사용자 정보 입력 시스템입니다.");

rl.question("이름을 입력하세요: ", (name) => {
  rl.question("나이를 입력하세요: ", (ageStr) => {
    const age = parseInt(ageStr, 10) || 0;
    rl.question("전화번호를입력하세요: ", (phone) => {
      console.log("\n--- 입력된 사용자 정보 ---");
      console.log("이름: " + name);
      console.log("나이: " + age);
      console.log("전화번호: " + phone);
      console.log("-------------------------");
      rl.close();
    });
  });
});
