# Release History

## 1.1.1 (2018-10-22)

- *timeout* property is added to the **AsistaOutput**.

## 1.1.0 (2018-09-25)

- Environment string for Environment.PROD changed from *PROD* to *PRODUCTION*. If you are using **Environment** you should update your *pyasista* version to keep things working.

## 1.0.1 (2018-08-13)

- Following static methods are added to *AsistaOutput* to create lambda outputs easier:
  - **AsistaOutput.with_stream(data):** Creates an instance of *AsistaOutput* with command PLAY_STREAM.
  - **AsistaOutput.with_announce(data):** Creates an instance of *AsistaOutput* with command PLAY_ANNOUNCE.
  - **AsistaOutput.with_stop():** Creates an instance of *AsistaOutput* with command STOP.
  - **AsistaOutput.with_noaction():** Creates an instance of *AsistaOutput* with command NOACTION.

## 1.0.0 (2018-08-10)

- Birth!