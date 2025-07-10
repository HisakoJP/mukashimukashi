const Alexa = require('ask-sdk-core');
const fs = require('fs'); // ファイルを読み込むためのモジュール
const path = require('path'); // ファイルパスを扱うためのモジュール

// =========================================================================================================================================
// ▼▼▼【プログラムの心臓部】▼▼▼
// 別のファイル『filelist.txt』から物語のリストを読み込みます。
// 今後、このファイル（index.js）を編集する必要はもうありません。
// =========================================================================================================================================
try {
  const filePath = path.join(__dirname, 'filelist.txt');
  const fileContent = fs.readFileSync(filePath, 'utf8');
  // ファイルの内容を一行ずつに分割し、空の行があれば無視する
  const fileNames = fileContent.split('\n').filter(line => line.trim() !== '');
  
  const baseUrl = 'https://HisakoJP.github.io/mukashimukashi/';
  var audioData = fileNames.map(fileName => {
    return {
      title: fileName.replace('.m4a', ''),
      url: baseUrl + fileName
    };
  });
} catch (e) {
  // もし filelist.txt が読み込めなかった場合は、スキルがエラーで止まらないようにダミーデータを用意しておく
  console.log('filelist.txtの読み込みに失敗しました。', e);
  var audioData = [{title: 'エラー', url: ''}];
}
// =========================================================================================================================================


// --- ここから下のコードは変更する必要はありません ---

// 配列からランダムに要素を取得するヘルパー関数
const getRandomItem = (array) => {
  const index = Math.floor(Math.random() * array.length);
  return array[index];
};


// スキル起動時のハンドラー
const LaunchRequestHandler = {
  canHandle(handlerInput) {
    return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
  },
  handle(handlerInput) {
    const randomAudio = getRandomItem(audioData);
    const speechText = `むかしむかしへようこそ。今日のお話は、${randomAudio.title}です。`;
    const token = randomAudio.url;

    return handlerInput.responseBuilder
      .speak(speechText)
      .addAudioPlayerPlayDirective('REPLACE_ALL', randomAudio.url, token, 0, null)
      .getResponse();
  }
};

// 「次のお話」などをリクエストされた時のハンドラー
const RandomAudioIntentHandler = {
  canHandle(handlerInput) {
    return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
      && Alexa.getIntentName(handlerInput.requestEnvelope) === 'RandomAudioIntent';
  },
  handle(handlerInput) {
    const randomAudio = getRandomItem(audioData);
    const speechText = `はい、次のお話ですね。${randomAudio.title}を再生します。`;
    const token = randomAudio.url;

    return handlerInput.responseBuilder
      .speak(speechText)
      .addAudioPlayerPlayDirective('REPLACE_ALL', randomAudio.url, token, 0, null)
      .getResponse();
  }
};

// ヘルプのハンドラー
const HelpIntentHandler = {
  canHandle(handlerInput) {
    return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
      && Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.HelpIntent';
  },
  handle(handlerInput) {
    const speechText = '「むかしむかしを開いて」と言うと、昔話をランダムに再生します。「次のお話」と言うと、別のお話を再生します。';

    return handlerInput.responseBuilder
      .speak(speechText)
      .reprompt(speechText)
      .getResponse();
  }
};

// キャンセル・ストップのハンドラー
const CancelAndStopIntentHandler = {
  canHandle(handlerInput) {
    return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
      && (Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.CancelIntent'
        || Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.StopIntent');
  },
  handle(handlerInput) {
    const speechText = 'さようなら。またお話を聞きに来てくださいね。';
    return handlerInput.responseBuilder
      .speak(speechText)
      .addAudioPlayerStopDirective()
      .getResponse();
  }
};

// セッション終了時のハンドラー
const SessionEndedRequestHandler = {
  canHandle(handlerInput) {
    return Alexa.getRequestType(handlerInput.requestEnvelope) === 'SessionEndedRequest';
  },
  handle(handlerInput) {
    console.log(`Session ended with reason: ${handlerInput.requestEnvelope.request.reason}`);
    return handlerInput.responseBuilder.getResponse();
  }
};

// エラーハンドラー
const ErrorHandler = {
  canHandle() {
    return true;
  },
  handle(handlerInput, error) {
    const speechText = 'すみません、うまく聞き取れませんでした。もう一度お試しください。';
    console.log(`Error handled: ${error.stack}`);

    return handlerInput.responseBuilder
      .speak(speechText)
      .reprompt(speechText)
      .getResponse();
  }
};

// スキルのビルダー
exports.handler = Alexa.SkillBuilders.custom()
  .addRequestHandlers(
    LaunchRequestHandler,
    RandomAudioIntentHandler,
    HelpIntentHandler,
    CancelAndStopIntentHandler,
    SessionEndedRequestHandler)
  .addErrorHandlers(
    ErrorHandler)
  .lambda();
