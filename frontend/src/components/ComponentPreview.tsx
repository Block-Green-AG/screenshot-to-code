import classNames from "classnames";
import ScreenshotToCodeComponent from "./GeneratedComponent";

interface Props {
  device: "mobile" | "desktop";
}

function ComponentPreview({ device }: Props) {
  return (
    <div className="flex justify-center mx-2">
      <div
        className={classNames(
          "border-[4px] border-black rounded-[20px] shadow-lg",
          "transform scale-[0.9] origin-top",
          {
            "w-full h-[832px]": device === "desktop",
            "w-[400px] h-[832px]": device === "mobile",
          }
        )}
      >
        <ScreenshotToCodeComponent />
      </div>
    </div>
  );
}

export default ComponentPreview;
