const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json());

// ✅ 정적 파일 제공: downloaded_images 폴더 사용
app.use('/static', express.static(path.join(__dirname, 'downloaded_images')));

// ✅ 폴더 안 이미지 파일 리스트 가져오기
app.get('/:folder/images', (req, res) => {
  const folder = req.params.folder;
  const dirPath = path.join(__dirname, 'downloaded_images', folder); // 여기도 변경

  fs.readdir(dirPath, (err, files) => {
    if (err) {
      return res.status(500).json({ error: '폴더를 읽을 수 없습니다.' });
    }
    const images = files.filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file));
    res.json(images);
  });
});


// 폴더별 노트 불러오기
app.get('/:folder/note', (req, res) => {
  const folder = req.params.folder;
  const notePath = path.join(__dirname, 'notes', `${folder}.txt`);

  fs.readFile(notePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(200).send('');
    }
    res.send(data);
  });
});

// 글 저장
app.post('/save', (req, res) => {
  const { folder, content } = req.body;
  const savePath = path.join(__dirname, 'notes', `${folder}.txt`);

  fs.writeFile(savePath, content, 'utf8', (err) => {
    if (err) {
      return res.status(500).json({ error: '저장 실패' });
    }
    res.json({ success: true });
  });
});

// 기본 페이지 (index.html)
app.get('/:folder', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`서버 실행 중: http://localhost:${PORT}`);
});

function getFolderList() {
    return fs.readdirSync(path.join(__dirname, 'downloaded_images'))
      .filter(item => fs.statSync(path.join(path.join(__dirname, 'downloaded_images'), item)).isDirectory()) // 디렉토리만 필터링
      .sort((a, b) => a - b); // 숫자 순으로 정렬
  }
const folders = getFolderList()
console.log(folders)

function getPrev(curr) {
    let left = 0;
    let right = folders.length - 1;
    let result = null;

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);

        if (parseInt(folders[mid]) < parseInt(curr)) {
            result = folders[mid]; // X보다 작은 값을 찾았을 때, 그 값을 기록
            left = mid + 1; // 더 큰 값을 찾기 위해 오른쪽 절반을 탐색
        } else {
            right = mid - 1; // X보다 작은 값이 없으면 왼쪽 절반을 탐색
        }
    }

    return result; // X보다 작은 값 반환, 없으면 -1
  }

function getNext(curr) {
    let left = 0;
    let right = folders.length - 1;
    let result = null;

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (parseInt(folders[mid]) > parseInt(curr)) {
            result = folders[mid]; // X보다 큰 값을 찾았을 때, 그 값을 기록
            right = mid - 1; // 더 작은 값을 찾기 위해 왼쪽 절반을 탐색
        } else {
            left = mid + 1; // X보다 큰 값이 없으면 오른쪽 절반을 탐색
        }
    }

    return result; // X보다 큰 값 반환, 없으면 null
  }

app.get('/:folder/prev', (req, res) => {
    const curr = req.params.folder;
    const prev = getPrev(curr);

    console.log(prev)
  
    if (prev) {
      res.json({ page: prev });
    } else {
      res.json({ page: folders[folders.length - 1] });;
    }
  });

app.get('/:folder/next', (req, res) => {
    const curr = req.params.folder;
    const next = getNext(curr);
  
    console.log(next)

    if (next) {
      res.json({ page: next });
    } else {
      res.json({ page: folders[0] });;
    }
  });